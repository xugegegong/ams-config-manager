"""Auth-related Pydantic schemas."""
from app.core.compat import CompatBaseModel as BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    display_name: str


class UserInfo(BaseModel):
    id: int
    username: str
    display_name: str
    is_admin: bool
