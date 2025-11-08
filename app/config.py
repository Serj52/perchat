import os
from typing import Any

from pydantic_settings import SettingsConfigDict, BaseSettings

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_URL: str | None = None

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, extra='ignore'
    )

    def model_post_init(self, __context: Any) -> None:
        if self.DB_URL is None:
            self.DB_URL = f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


class AuthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, extra='ignore'
    )


AUTH_SETTINGS = AuthSettings().model_dump()
DB_SETTINGS = DbSettings().model_dump()
print()
