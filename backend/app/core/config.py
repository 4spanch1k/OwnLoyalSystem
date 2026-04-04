from functools import lru_cache
import os

from pydantic import BaseModel

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ModuleNotFoundError:
    BaseSettings = BaseModel

    def SettingsConfigDict(**kwargs: object) -> dict[str, object]:
        return kwargs


class Settings(BaseSettings):
    app_name: str = "AzamatAI Loyalty Backend"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    default_currency_code: str = "KZT"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/azamatai"

    model_config = SettingsConfigDict(
        env_prefix="AZAMAT_",
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("AZAMAT_APP_NAME", "AzamatAI Loyalty Backend"),
        app_version=os.getenv("AZAMAT_APP_VERSION", "0.1.0"),
        api_v1_prefix=os.getenv("AZAMAT_API_V1_PREFIX", "/api/v1"),
        default_currency_code=os.getenv("AZAMAT_DEFAULT_CURRENCY_CODE", "KZT"),
        database_url=os.getenv(
            "DATABASE_URL",
            os.getenv(
                "AZAMAT_DATABASE_URL",
                "postgresql+psycopg://postgres:postgres@localhost:5432/azamatai",
            ),
        ),
    )
