from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets
from pydantic_core import MultiHostUrl
from pydantic import (
    PostgresDsn,
    computed_field,
)

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    
    # JWT Tokens
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30   # 8 days = 8 days * 60 minutes * 24 hours 


    # Postgres
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

settings = Settings()