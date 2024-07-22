from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """アプリケーションの設定情報"""

    RUN_ENV: str = Field(default="local")
    APP_NAME: str = Field(default="cpp-coconala")
    VERSION: str = "0.0.1"
    DEBUG: bool = Field(default=False)
    BASE_URL: str = Field(default="http://localhost:8000")
    API_ROOT_PATH: str = Field(default="/api")
    CLIENT_URL: str = Field(default="http://localhost:3000")
    LOG_CONFIG_PATH: str = Field(default="src/core//settings/logs/logger_config.yml")

    # データベース接続情報
    DB_HOST: str = Field(default="db")
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str = Field(default="5432")
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        """
        環境編巣を加工して使うときは
        pydanticが環境変数をロードしてからでないとエラーになる
        """

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # CORS 適時追加すること
    ORIGIN_RESOURCES: list[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


@lru_cache
def get_settings(env_file: str = ".env") -> AppSettings:
    return AppSettings()  # type: ignore


settings = get_settings()
