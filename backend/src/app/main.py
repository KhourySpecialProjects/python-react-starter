import uvicorn
from fastapi import FastAPI
from pydantic.alias_generators import to_camel

from app.config.logger import configure_logging
from app.config.settings import settings
from app.middleware.request_logger import log_requests
from app.routes import api_router

configure_logging()

app = FastAPI(
    title="API",
    version="1.0.0",
    # The spec is only written to backend/openapi.json. No docs pages are served.
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
    # The handler name in camelCase becomes the operationId, so the generated
    # frontend client gets listMessages() instead of listMessagesApiV1MessagesGet().
    generate_unique_id_function=lambda route: to_camel(route.name),
)
app.middleware("http")(log_requests)
app.include_router(api_router)


if __name__ == "__main__":
    development = settings.environment == "development"
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1" if development else "0.0.0.0",
        port=settings.port,
        reload=development,
        log_config=None,
    )
