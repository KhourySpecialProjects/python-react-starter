from fastapi import APIRouter

from app.routes import health, messages

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(messages.router)
