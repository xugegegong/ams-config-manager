"""Database connection related schemas."""
from app.core.compat import CompatBaseModel as BaseModel


class DBConnectRequest(BaseModel):
    host: str = "192.168.8.48"
    port: int = 3306
    username: str = "root"
    password: str = ""
    database: str = "hlx"


class DBConnectResponse(BaseModel):
    success: bool
    message: str
    server_version: str = ""
