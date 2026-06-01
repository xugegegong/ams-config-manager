"""Application configuration."""
from typing import Optional

try:
    # Pydantic v2
    from pydantic_settings import BaseSettings
except ImportError:
    # Pydantic v1
    from pydantic import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AMS Config Manager"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 hours

    # Default database (the system's own config DB)
    # Use SQLite for development; change to MySQL for production
    DATABASE_URL: str = "sqlite:///./ams_config.db"

    # Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
