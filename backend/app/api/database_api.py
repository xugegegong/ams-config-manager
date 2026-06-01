"""Database connection test API (connects to target ship database)."""
import pymysql
from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.database import DBConnectRequest, DBConnectResponse

router = APIRouter(prefix="/api/database", tags=["database"])


@router.post("/test-connection", response_model=DBConnectResponse)
def test_connection(
    req: DBConnectRequest,
    current_user: User = Depends(get_current_user),
):
    """Test MySQL connection with provided credentials."""
    try:
        conn = pymysql.connect(
            host=req.host,
            port=req.port,
            user=req.username,
            password=req.password,
            database=req.database,
            connect_timeout=5,
        )
        version = conn.get_server_info()
        conn.close()
        return DBConnectResponse(
            success=True,
            message="连接成功",
            server_version=version,
        )
    except Exception as e:
        return DBConnectResponse(
            success=False,
            message=f"连接失败: {str(e)}",
        )
