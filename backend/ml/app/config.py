from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    REDIS_URL: str
    HIVE_SERVICE_URL: str
    ML_SERVICE_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
