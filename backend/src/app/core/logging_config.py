import json
import logging
import logging.config
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Literal

# Set per request by RequestLoggingMiddleware, so every log line written while
# handling a request (from any module) carries the same id.
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")

# Attributes every LogRecord has. Anything else was passed with `extra=`.
# uvicorn adds color_message, an ANSI-colored copy of the message.
_STANDARD_ATTRS = set(vars(logging.makeLogRecord({}))) | {
    "message",
    "request_id",
    "color_message",
}


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


class JsonFormatter(logging.Formatter):
    """One JSON object per line, including any `extra=` fields."""

    def format(self, record: logging.LogRecord) -> str:
        entry: dict[str, object] = {
            "time": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
        }
        for key, value in vars(record).items():
            if key not in _STANDARD_ATTRS:
                entry[key] = value
        if record.exc_info:
            entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(entry, default=str)


def configure_logging(level: str, log_format: Literal["text", "json"]) -> None:
    """Send app and uvicorn logs through one handler on stdout."""
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {"request_id": {"()": RequestIdFilter}},
            "formatters": {
                "text": {
                    "format": "%(asctime)s %(levelname)-7s [%(request_id)s] "
                    "%(name)s: %(message)s"
                },
                "json": {"()": JsonFormatter},
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": log_format,
                    "filters": ["request_id"],
                }
            },
            "root": {"level": level, "handlers": ["stdout"]},
            "loggers": {
                # Re-route uvicorn's own loggers to the root handler above.
                "uvicorn": {"handlers": [], "propagate": True},
                "uvicorn.error": {"handlers": [], "propagate": True},
                # RequestLoggingMiddleware replaces uvicorn's access log.
                "uvicorn.access": {"handlers": [], "propagate": False},
            },
        }
    )
