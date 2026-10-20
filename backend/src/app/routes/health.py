from fastapi import APIRouter
from sqlalchemy import text

from app.config.db import SessionDep
from app.schemas.health import Health

router = APIRouter()


@router.get("/health", response_description="The API and database are reachable")
async def get_health(session: SessionDep) -> Health:
    await session.execute(text("SELECT 1"))
    return Health(status="ok")
