from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Read from environment variables, e.g. DATABASE_URL and LOG_LEVEL."""

    environment: Literal["development", "production"] = "production"
    database_url: str
    port: int = 3000
    log_level: Literal["debug", "info", "warning", "error"] = "info"


settings = Settings()
