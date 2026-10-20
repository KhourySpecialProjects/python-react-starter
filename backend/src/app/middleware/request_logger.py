import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

logger = logging.getLogger("app.requests")


def level_for(status: int) -> int:
    if status >= 500:
        return logging.ERROR
    if status >= 400:
        return logging.WARNING
    return logging.INFO


async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start = time.perf_counter()
    response = await call_next(request)

    status = response.status_code
    if request.url.path == "/api/v1/health" and status < 400:
        return response

    duration_ms = round((time.perf_counter() - start) * 1000)
    logger.log(
        level_for(status),
        "%s %s %d %dms",
        request.method,
        request.url.path,
        status,
        duration_ms,
    )
    return response
