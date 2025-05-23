from typing import Any

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core.core_schema import ValidationInfo
from pydantic import PostgresDsn, field_validator


class Settings(BaseSettings):
    ROOT_DIR: Path = Path(__file__).parent.parent.parent.resolve()

    POSTGRES_HOST: str = "db_dev"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres"
    POSTGRES_USERNAME: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    
    POSTGRES_URL: str = ""

    SALT: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    @field_validator("POSTGRES_URL", mode="before")
    @classmethod
    def assemble_postgres_url(cls, v: Any, info: ValidationInfo) -> str:
        if isinstance(v, str) and v:
            return v

        postgres_dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data["POSTGRES_USERNAME"],
            password=info.data["POSTGRES_PASSWORD"],
            host=info.data["POSTGRES_HOST"],
            port=info.data["POSTGRES_PORT"],
            path=info.data["POSTGRES_DB"],
        )
        return str(postgres_dsn)


    model_config = SettingsConfigDict(
        env_file=(f"{ROOT_DIR}/.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_assignment=True,
        extra="ignore",
    )


settings = Settings()
