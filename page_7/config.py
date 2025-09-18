from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    BASE_DIR: Path = Path(__file__).resolve()
    ENVIRONMENT: str = 'dev'
    LOG_LEVEL: str = 'DEBUG'
    APP_TITLE: str = 'MY_APP'
    APP_VERSION: str = '0.2.0'
    API_PREFIX: str = 'api'
    API_VERSION: str = 'v1'


if __name__ == '__main__':
    settings = Settings()
    print(settings.model_dump_json(indent=4))
