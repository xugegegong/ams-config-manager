"""Modbus and signal point related schemas."""
from app.core.compat import CompatBaseModel as BaseModel
from typing import Optional, List


class ModbusConfigCreate(BaseModel):
    channel_id: int
    name: str
    comm_type: str = "Modbus"
    transport_mode: str = "TCP"
    electrical_interface: str = ""
    baud_rate: int = 19200
    data_bits: int = 8
    stop_bits: int = 1
    parity: str = "None"
    slave_id: int = 1
    func_code_read_di: int = 1
    func_code_read_ai: int = 3
    ip_address: str = ""
    port: int = 502


class ModbusConfigResponse(BaseModel):
    id: int
    name: str
    comm_type: str
    transport_mode: str
    baud_rate: int
    slave_id: int
    ip_address: str
    port: int
    points_count: int = 0


class SignalPointCreate(BaseModel):
    modbus_config_id: int
    point_index: Optional[int] = None
    name: str
    modbus_address: str
    signal_type: str = "开关量"
    alarm_on_1: Optional[str] = "报警"
    display_normal: Optional[str] = "正常"
    display_alarm: Optional[str] = "报警"
    unit: Optional[str] = ""
    data_type: Optional[str] = ""
    byte_order: Optional[str] = ""
    coefficient: Optional[str] = "0,1,0"
    ams_module_id: Optional[str] = ""
    is_active: int = 1


class SignalPointResponse(BaseModel):
    id: int
    point_index: Optional[int]
    name: str
    modbus_address: str
    signal_type: str
    unit: Optional[str]
    data_type: Optional[str]
    ams_module_id: Optional[str]
    is_active: int


class ConfigGenerateResponse(BaseModel):
    success: bool
    message: str
    json_content: Optional[dict] = None
    txt_content: Optional[str] = None
    file_paths: Optional[dict] = None
