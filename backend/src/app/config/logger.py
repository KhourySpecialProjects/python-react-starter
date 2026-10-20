import logging

from rich.logging import RichHandler

from app.config.settings import settings


def configure_logging() -> None:
    """Colored logs from rich in development, plain lines in production.
    uvicorn's logs go through the same handler."""
    development = settings.environment == "development"
    logging.basicConfig(
        level=settings.log_level.upper(),
        handlers=[
            RichHandler(rich_tracebacks=True)
            if development
            else logging.StreamHandler()
        ],
        format="%(message)s"
        if development
        else "%(asctime)s %(levelname)s %(name)s: %(message)s",
        force=True,
    )
    # The request logger middleware replaces uvicorn's access log.
    logging.getLogger("uvicorn.access").disabled = True
