from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    COOKIE_NAME: str = "access_token"
    COOKIE_SECURE: bool = False
    DOMAIN: str = "localhost"
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: List[str] = ["http://localhost:8080", "http://localhost:5173"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
