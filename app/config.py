import os
from typing import Any

from pydantic_settings import SettingsConfigDict, BaseSettings

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_URL: str = None

    model_config = SettingsConfigDict(
        env_file=ENV_PATH
    )

    def model_post_init(self, __context: Any) -> None:
        if self.DB_URL is None:
            self.DB_URL = f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


class AuthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    model_config = SettingsConfigDict(
        env_file=ENV_PATH
    )


auth_settings = AuthSettings()
db_settings = DbSettings()


def get_auth_settings():
    return {"secret_key": auth_settings.SECRET_KEY, "algorithm": auth_settings.ALGORITHM}

def get_db_settings():
    return {"db_url": db_settings.DB_URL}
