import os

from enum import Enum
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Environment(Enum):
    TEST = 'test'
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


class TestSettings(Settings):
    ENVIRONMENT: Environment = Environment.TEST
    LOG_LEVEL: LogLevel = LogLevel.DEBUG

    APP_TITLE: str = 'MY_APP_TEST'

    KEYCLOAK_SERVER_URL: str = 'https://isso-dev.mts.ru/auth'
    KEYCLOAK_CLIENT_ID: str = 'dev_client_id'


class DevSettings(Settings):
    ENVIRONMENT: Environment = Environment.DEV
    LOG_LEVEL: LogLevel = LogLevel.DEBUG

    APP_TITLE: str = 'MY_APP_DEV'

    KEYCLOAK_SERVER_URL: str = 'https://isso-dev.mts.ru/auth'
    KEYCLOAK_CLIENT_ID: str = 'dev_client_id'


class ProdSettings(Settings):
    ENVIRONMENT: Environment = Environment.PROD
    LOG_LEVEL: LogLevel = LogLevel.INFO

    APP_TITLE: str = 'MY_APP'

    KEYCLOAK_SERVER_URL: str = 'https://iss.mts.ru/auth'
    KEYCLOAK_CLIENT_ID: str = 'prod_client_id'


ENVIRONMENTS: dict[str | None, type[Settings]] = {
    Environment.TEST.value: TestSettings,
    Environment.DEV.value: DevSettings,
    Environment.PROD.value: ProdSettings,
}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    env = os.environ.get('ENVIRONMENT')
    return ENVIRONMENTS[env]()  # type: ignore[reportCallIssue]


if __name__ == '__main__':
    settings = get_settings()
    print(settings.model_dump_json(indent=4))
