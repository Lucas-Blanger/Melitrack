from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Database components
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: int

    # Database URL
    DATABASE_URL: str | None = None

    # Mongo DB config
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_URL: str
    MONGO_DB: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # API
    APP_NAME: str
    APP_VERSION: str
    API_PORT: int
    DEBUG: bool
    COOKIE_SECURE: bool

    # Rate limit
    RATE_LIMIT_ENABLED: bool
    RATE_LIMIT_DEFAULT_REQUESTS: int
    RATE_LIMIT_DEFAULT_WINDOW_SECONDS: int
    RATE_LIMIT_AUTH_LOGIN_REQUESTS: int
    RATE_LIMIT_AUTH_LOGIN_WINDOW_SECONDS: int
    RATE_LIMIT_AUTH_REGISTER_REQUESTS: int
    RATE_LIMIT_AUTH_REGISTER_WINDOW_SECONDS: int
    RATE_LIMIT_AUTH_PASSWORD_RESET_REQUESTS: int
    RATE_LIMIT_AUTH_PASSWORD_RESET_WINDOW_SECONDS: int

    # Email config
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM: str

    # CORS
    ALLOWED_ORIGINS: list[str]

    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL

        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
