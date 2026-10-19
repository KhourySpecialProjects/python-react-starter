import logging
import time
import uuid

from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.logging_config import request_id_var

logger = logging.getLogger("app.requests")

# Docker polls this every few seconds; logging it would bury real requests.
QUIET_PATHS = {"/api/v1/health"}


class RequestLoggingMiddleware:
    """Give each request an id and log one line when it finishes.

    Written as plain ASGI middleware rather than `@app.middleware("http")`,
    which wraps responses in a way that breaks streaming and context variables.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = uuid.uuid4().hex
        request_id_var.set(request_id)
        start = time.perf_counter()
        status = 500

        async def send_with_request_id(message: Message) -> None:
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
                message.setdefault("headers", []).append(
                    (b"x-request-id", request_id.encode())
                )
            await send(message)

        try:
            await self.app(scope, receive, send_with_request_id)
        finally:
            # On an unhandled error, status stays 500 and uvicorn logs the
            # traceback right after this line, with the same request id.
            if scope["path"] not in QUIET_PATHS:
                duration_ms = round((time.perf_counter() - start) * 1000, 1)
                logger.log(
                    logging.ERROR if status >= 500 else logging.INFO,
                    "%s %s %d %.1fms",
                    scope["method"],
                    scope["path"],
                    status,
                    duration_ms,
                    extra={
                        "method": scope["method"],
                        "path": scope["path"],
                        "status": status,
                        "duration_ms": duration_ms,
                    },
                )
