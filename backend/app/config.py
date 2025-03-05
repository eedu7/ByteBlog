from pathlib import Path

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"


class Config(BaseConfig):
    POSTGRES_URL: str
    TEST_POSTGRES_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15 * 24  # one Day
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days


config = Config()
