from enum import Enum
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Environment(Enum):
    DEV = 'dev'
    PROD = 'prod'


class LogLevel(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class DatabeseSettings(BaseModel):
    HOST: str
    PORT: str
    USER: str
    PASS: str
    NAME: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    BASE_DIR: Path = Path(__file__).resolve()

    ENVIRONMENT: Environment = Environment.DEV
    LOG_LEVEL: LogLevel = LogLevel.DEBUG

    APP_TITLE: str = 'MY_APP'
    APP_VERSION: str = '0.2.0'
    API_PREFIX: str = 'api'
    API_VERSION: str = 'v1'

    DB: DatabeseSettings


if __name__ == '__main__':
    settings = Settings()  # type: ignore[reportCallIssue]
    print(settings.model_dump_json(indent=4))
