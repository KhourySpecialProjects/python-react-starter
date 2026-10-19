from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Read from environment variables, e.g. DATABASE_URL and LOG_LEVEL."""

    database_url: str
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    # "json" for deployed environments, so a log service can parse each line.
    log_format: Literal["text", "json"] = "text"


settings = Settings()
