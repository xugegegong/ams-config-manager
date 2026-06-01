"""Modbus configuration API routes."""
import json
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.ship_config import (
    Ship, Gateway, Channel, ModbusConfig, SignalPoint,
)
from app.schemas.modbus import (
    ModbusConfigCreate, ModbusConfigResponse,
    SignalPointCreate, SignalPointResponse,
    ConfigGenerateResponse,
)

router = APIRouter(prefix="/api/modbus", tags=["modbus"])


# ─── Ships ───
@router.get("/ships")
def list_ships(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ships = db.query(Ship).all()
    return [
        {"id": s.id, "name": s.name, "imo": s.imo, "mmsi": s.mmsi}
        for s in ships
    ]


@router.post("/ships")
def create_ship(name: str, imo: str = "", mmsi: str = "",
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    ship = Ship(name=name, imo=imo, mmsi=mmsi)
    db.add(ship)
    db.commit()
    db.refresh(ship)
    return {"id": ship.id, "name": ship.name}


# ─── Gateways (SailingData / EngineData) ───
@router.get("/gateways/{ship_id}")
def list_gateways(ship_id: int, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    gateways = db.query(Gateway).filter(Gateway.ship_id == ship_id).all()
    return [
        {"id": g.id, "name": g.name, "way_uid": g.way_uid, "way_type": g.way_type}
        for g in gateways
    ]


# ─── Modbus Configs ───
@router.get("/configs/{channel_id}", response_model=List[ModbusConfigResponse])
def list_modbus_configs(channel_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    configs = db.query(ModbusConfig).filter(ModbusConfig.channel_id == channel_id).all()
    result = []
    for c in configs:
        points_count = db.query(SignalPoint).filter(
            SignalPoint.modbus_config_id == c.id
        ).count()
        result.append(ModbusConfigResponse(
            id=c.id, name=c.name, comm_type=c.comm_type,
            transport_mode=c.transport_mode, baud_rate=c.baud_rate,
            slave_id=c.slave_id, ip_address=c.ip_address, port=c.port,
            points_count=points_count,
        ))
    return result


@router.post("/configs")
def create_modbus_config(
    req: ModbusConfigCreate, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    config = ModbusConfig(**req.dict())
    db.add(config)
    db.commit()
    db.refresh(config)
    return {"id": config.id, "name": config.name}


@router.put("/configs/{config_id}")
def update_modbus_config(
    config_id: int, req: ModbusConfigCreate, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    config = db.query(ModbusConfig).filter(ModbusConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    for key, val in req.dict().items():
        setattr(config, key, val)
    db.commit()
    return {"id": config.id, "name": config.name}


@router.delete("/configs/{config_id}")
def delete_modbus_config(config_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    config = db.query(ModbusConfig).filter(ModbusConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    db.delete(config)
    db.commit()
    return {"message": "已删除"}


# ─── Signal Points ───
@router.get("/points/{config_id}", response_model=List[SignalPointResponse])
def list_points(config_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    points = db.query(SignalPoint).filter(
        SignalPoint.modbus_config_id == config_id
    ).order_by(SignalPoint.point_index).all()
    return points


@router.post("/points")
def create_point(req: SignalPointCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    point = SignalPoint(**req.dict())
    db.add(point)
    db.commit()
    db.refresh(point)
    return {"id": point.id, "name": point.name}


@router.put("/points/{point_id}")
def update_point(point_id: int, req: SignalPointCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    point = db.query(SignalPoint).filter(SignalPoint.id == point_id).first()
    if not point:
        raise HTTPException(status_code=404, detail="工况点不存在")
    for key, val in req.dict().items():
        setattr(point, key, val)
    db.commit()
    return {"id": point.id, "name": point.name}


@router.delete("/points/{point_id}")
def delete_point(point_id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    point = db.query(SignalPoint).filter(SignalPoint.id == point_id).first()
    if not point:
        raise HTTPException(status_code=404, detail="工况点不存在")
    db.delete(point)
    db.commit()
    return {"message": "已删除"}


# ─── Batch Operations ───
@router.post("/points/batch/{config_id}")
def batch_save_points(config_id: int, points: List[SignalPointCreate],
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """批量保存工况点（先删后插，全量替换）"""
    db.query(SignalPoint).filter(SignalPoint.modbus_config_id == config_id).delete()
    for p in points:
        point = SignalPoint(**p.dict())
        db.add(point)
    db.commit()
    return {"message": f"已保存 {len(points)} 个工况点"}


# ─── Generate Config ───
@router.post("/generate/{config_id}", response_model=ConfigGenerateResponse)
def generate_config(config_id: int, output_dir: str = "./generated",
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    """生成 Modbus 配置文件（JSON + TXT）"""
    config = db.query(ModbusConfig).filter(ModbusConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")

    points = db.query(SignalPoint).filter(
        SignalPoint.modbus_config_id == config_id,
        SignalPoint.is_active == 1,
    ).order_by(SignalPoint.point_index).all()

    # Build JSON config matching original format
    results = []
    for p in points:
        item = {
            "Addr": p.modbus_address,
            "Alias": p.ams_module_id or p.modbus_address,
            "Coefficient": p.coefficient or "0,1,0",
            "DataLen": "1",
            "DataTypeRegister": "2",
        }
        results.append(item)

    json_config = {
        "ChanCode": str(config.channel_id),
        "ChanDesc": config.name,
        "ChanType": "7",
        "DataProtocol": "6",
        "NetModTcp": [
            {
                "DataLen": str(len(points)),
                "DevName": config.name,
                "FunCode": str(config.func_code_read_ai),
                "RegisterBegin": str(points[0].modbus_address) if points else "40001",
                "Results": results,
                "SlaveId": str(config.slave_id).zfill(2),
            }
        ],
        "WayUid": "",
    }

    # Generate TXT: comma-separated address list
    txt_content = ",".join(p.modbus_address for p in points)

    # Ensure output dir
    os.makedirs(output_dir, exist_ok=True)

    json_path = os.path.join(output_dir, f"{config.name}.json")
    txt_path = os.path.join(output_dir, f"{config.name}.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_config, f, ensure_ascii=False, indent=4)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(txt_content)

    return ConfigGenerateResponse(
        success=True,
        message=f"配置已生成: {json_path}, {txt_path}",
        json_content=json_config,
        txt_content=txt_content,
        file_paths={"json": json_path, "txt": txt_path},
    )
