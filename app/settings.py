from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    DB_NAME: str
    SERVICE_NAME: str
    SERVICE_HOST: str
    SERVICE_PORT: int
    SECRET_TOKEN: str
    ENCRYPTION_ALGORITHM: str
    TIME_EXPIRES: int
    model_config = {
        "extra": "ignore"
    }

settings = AppSettings(_env_file='.env', _env_file_encoding='utf-8') # type: ignore