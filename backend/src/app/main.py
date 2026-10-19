from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.core.db import engine
from app.core.logging_config import configure_logging
from app.core.middleware import RequestLoggingMiddleware
from app.core.settings import settings
from app.routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with httpx.AsyncClient(timeout=10) as http_client:
        app.state.http_client = http_client
        yield
    await engine.dispose()


def operation_id(route: APIRoute) -> str:
    """Use the handler's name as the OpenAPI operationId, so the generated
    frontend client gets `listNotes()` instead of `listNotesApiV1NotesGet()`."""
    return route.name


def create_app() -> FastAPI:
    configure_logging(settings.log_level, settings.log_format)

    app = FastAPI(
        title="Starter API",
        lifespan=lifespan,
        docs_url="/api/v1/docs",
        openapi_url="/api/v1/openapi.json",
        generate_unique_id_function=operation_id,
    )
    app.add_middleware(RequestLoggingMiddleware)
    app.include_router(api_router)
    return app


app = create_app()
