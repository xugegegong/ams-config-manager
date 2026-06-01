"""Authentication API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
)
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, UserInfo

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已禁用",
        )
    token = create_access_token(data={"sub": user.username})
    return TokenResponse(
        access_token=token,
        username=user.username,
        display_name=user.display_name or user.username,
    )


@router.get("/me", response_model=UserInfo)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/init-admin")
def init_admin(db: Session = Depends(get_db)):
    """Initialize default admin user (call once on first setup)."""
    existing = db.query(User).filter(User.username == "admin").first()
    if existing:
        return {"message": "Admin already exists"}
    admin = User(
        username="admin",
        hashed_password=get_password_hash("admin123"),
        display_name="管理员",
        is_active=True,
        is_admin=True,
    )
    db.add(admin)
    db.commit()
    return {"message": "Admin created (username=admin, password=admin123)"}
