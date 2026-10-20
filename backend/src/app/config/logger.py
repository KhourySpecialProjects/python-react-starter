import logging
from datetime import datetime

from rich.console import Console
from rich.text import Text

from app.config.settings import settings


class ColorHandler(logging.Handler):
    """One colored line per log record, printed with rich.

    rich's own RichHandler lays logs out in fixed-width columns, and behind
    mise's [dev:backend] prefix it can't measure the terminal, so it wraps every
    long line. Printing a single line lets the terminal do the wrapping."""

    def __init__(self) -> None:
        super().__init__()
        self.console = Console(soft_wrap=True)

    def emit(self, record: logging.LogRecord) -> None:
        time = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        self.console.print(
            Text(time, style="dim"),
            Text(
                f"{record.levelname:<7}",
                style=f"logging.level.{record.levelname.lower()}",
            ),
            self.console.highlighter(self.format(record)),
        )


def configure_logging() -> None:
    """Colored logs in development, plain lines in production. uvicorn's logs
    go through the same handler."""
    development = settings.environment == "development"
    logging.basicConfig(
        level=settings.log_level.upper(),
        handlers=[ColorHandler() if development else logging.StreamHandler()],
        format="%(message)s"
        if development
        else "%(asctime)s %(levelname)s %(message)s",
        force=True,
    )
    # The request logger middleware replaces uvicorn's access log.
    logging.getLogger("uvicorn.access").disabled = True
