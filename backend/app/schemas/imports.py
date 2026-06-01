"""Excel import and version diff related schemas."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ColumnMapping(BaseModel):
    """列映射: 系统字段名 → Excel 列字母"""
    name: str = "B"          # 名称
    modbus_address: str = "C"  # Modbus地址
    signal_type: str = "D"     # 信号类型
    point_index: str = "A"     # 序号
    alarm_on_1: Optional[str] = None  # 报警状态(1断开)
    display_normal: Optional[str] = None
    display_alarm: Optional[str] = None
    unit: Optional[str] = None
    data_type: Optional[str] = None
    byte_order: Optional[str] = None
    ams_module_id: Optional[str] = None
    coefficient: Optional[str] = None


class ImportTemplateCreate(BaseModel):
    name: str
    manufacturer: str = ""
    ship_series: str = ""
    description: str = ""
    column_mapping: ColumnMapping
    header_row: int = 7
    data_start_row: int = 8
    comm_params_row: int = 1


class ImportTemplateResponse(BaseModel):
    id: int
    name: str
    manufacturer: str
    ship_series: str
    column_mapping: Dict[str, Any]
    description: str

    class Config:
        orm_mode = True


class ExcelPreview(BaseModel):
    columns: List[str]
    rows: List[List[Any]]
    total_rows: int
    total_cols: int


class ChangeItem(BaseModel):
    change_type: str  # added / deleted / modified
    point_name: str
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    diff_fields: Optional[List[Dict[str, Any]]] = None


class VersionDiffResponse(BaseModel):
    old_version: str
    new_version: str
    added: List[Dict[str, Any]]
    deleted: List[Dict[str, Any]]
    modified: List[Dict[str, Any]]


class BatchApproveRequest(BaseModel):
    action: str  # accept_all / reject_all
    change_ids: Optional[List[int]] = None
