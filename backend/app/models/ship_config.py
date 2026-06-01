"""Core business models: ships, gateways, channels, device configs, versions."""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON, func
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Ship(Base):
    """船舶"""
    __tablename__ = "ships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False, comment="船名")
    imo = Column(String(32), comment="IMO编号")
    mmsi = Column(String(32), comment="MMSI")
    description = Column(Text, comment="备注")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    gateways = relationship("Gateway", back_populates="ship", cascade="all, delete-orphan")


class Gateway(Base):
    """网关（数据通路）：对应原系统的 ways 表"""
    __tablename__ = "gateways"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ship_id = Column(Integer, ForeignKey("ships.id"), nullable=False)
    way_uid = Column(String(56), comment="网关唯一标识")
    name = Column(String(56), nullable=False, comment="网关名称: SailingData / EngineData")
    way_type = Column(Integer, default=3, comment="类型")
    way_index = Column(String(56), comment="索引")
    ip = Column(String(56), default="")
    server_ip = Column(String(56), default="")
    mask = Column(String(56), default="")
    default_gateway = Column(String(56), default="")
    channels_num = Column(Integer, default=0)

    ship = relationship("Ship", back_populates="gateways")
    channels = relationship("Channel", back_populates="gateway", cascade="all, delete-orphan")


class Channel(Base):
    """通道：对应 channelsdataprotocol 表"""
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gateway_id = Column(Integer, ForeignKey("gateways.id"), nullable=False)
    chan_code = Column(Integer, nullable=False, comment="通道编号")
    chan_type = Column(Integer, default=7, comment="通道类型")
    chan_name = Column(String(56), default="", comment="通道名称")
    data_protocol = Column(Integer, default=1, comment="协议: 1=NMEA, 2=Modbus RTU, 6=Modbus TCP")
    json_config = Column(JSON, comment="原始JSON配置")

    gateway = relationship("Gateway", back_populates="channels")
    modbus_configs = relationship("ModbusConfig", back_populates="channel", cascade="all, delete-orphan")


class ModbusConfig(Base):
    """Modbus 客户端配置"""
    __tablename__ = "modbus_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    name = Column(String(128), comment="客户端名称")

    # 通讯参数
    comm_type = Column(String(32), default="Modbus", comment="通讯类型")
    transport_mode = Column(String(16), default="TCP", comment="传输模式: TCP/RTU")
    electrical_interface = Column(String(64), default="", comment="电气接口")
    baud_rate = Column(Integer, default=19200, comment="波特率")
    data_bits = Column(Integer, default=8, comment="数据位")
    stop_bits = Column(Integer, default=1, comment="停止位")
    parity = Column(String(8), default="None", comment="校验位: None/Even/Odd")
    slave_id = Column(Integer, default=1, comment="从站地址")
    func_code_read_di = Column(Integer, default=1, comment="读取开关量功能码")
    func_code_read_ai = Column(Integer, default=3, comment="读取模拟量功能码")
    ip_address = Column(String(64), default="", comment="TCP模式时的IP")
    port = Column(Integer, default=502, comment="TCP模式时的端口")

    channel = relationship("Channel", back_populates="modbus_configs")
    points = relationship("SignalPoint", back_populates="modbus_config", cascade="all, delete-orphan")


class SignalPoint(Base):
    """工况点（信号点）"""
    __tablename__ = "signal_points"

    id = Column(Integer, primary_key=True, autoincrement=True)
    modbus_config_id = Column(Integer, ForeignKey("modbus_configs.id"), nullable=False)
    version_id = Column(Integer, ForeignKey("config_versions.id"), nullable=True)

    # 基础信息
    point_index = Column(Integer, comment="序号")
    name = Column(String(256), nullable=False, comment="名称")
    modbus_address = Column(String(32), nullable=False, comment="Modbus地址")
    signal_type = Column(String(16), default="开关量", comment="信号类型: 开关量/模拟量/浮点数")

    # 开关量专用
    alarm_on_1 = Column(String(32), default="报警", comment="1断开报警0闭合报警")
    display_normal = Column(String(32), default="正常", comment="正常显示")
    display_alarm = Column(String(32), default="报警", comment="报警显示")

    # 模拟量专用
    unit = Column(String(16), default="", comment="单位")
    data_type = Column(String(32), default="", comment="数据类型: 浮点数/整数等")
    byte_order = Column(String(16), default="", comment="字节顺序: 1234/4321等")
    coefficient = Column(String(32), default="0,1,0", comment="系数")

    # AMS 模块编号
    ams_module_id = Column(String(64), default="", comment="AMS模块数据编号")

    # 状态
    is_active = Column(Integer, default=1, comment="是否有效: 1有效, 0备用/删除")

    modbus_config = relationship("ModbusConfig", back_populates="points")


class ConfigVersion(Base):
    """配置版本记录（用于版本比对）"""
    __tablename__ = "config_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    modbus_config_id = Column(Integer, ForeignKey("modbus_configs.id"), nullable=False)
    version_tag = Column(String(32), nullable=False, comment="版本号: V1.0, V2.0")
    source_file = Column(String(256), comment="来源文件名")
    change_summary = Column(Text, comment="变更摘要")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class VersionChange(Base):
    """版本变更明细"""
    __tablename__ = "version_changes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version_id = Column(Integer, ForeignKey("config_versions.id"), nullable=False)
    point_id = Column(Integer, ForeignKey("signal_points.id"), nullable=True)
    change_type = Column(String(16), nullable=False, comment="变更类型: added/deleted/modified")
    field_name = Column(String(64), default="", comment="修改的字段名")
    old_value = Column(Text, default="", comment="旧值")
    new_value = Column(Text, default="", comment="新值")
    status = Column(String(16), default="pending", comment="审批状态: pending/accepted/rejected")
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class ImportTemplate(Base):
    """Excel 导入模板（列映射配置）"""
    __tablename__ = "import_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False, comment="模板名称")
    manufacturer = Column(String(128), default="", comment="AMS厂商")
    ship_series = Column(String(128), default="", comment="船型系列")
    description = Column(Text, comment="描述")

    # 列映射: JSON格式 {"名称": "B", "Modbus地址": "C", ...}
    column_mapping = Column(JSON, nullable=False, comment="列映射配置")
    header_row = Column(Integer, default=7, comment="表头行号")
    data_start_row = Column(Integer, default=8, comment="数据起始行号")
    comm_params_row = Column(Integer, default=1, comment="通讯参数起始行")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
