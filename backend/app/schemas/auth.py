"""Auth-related Pydantic schemas."""
from pydantic import BaseModel


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

    class Config:
        orm_mode = True
