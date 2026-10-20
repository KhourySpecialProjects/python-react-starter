from fastapi import APIRouter

from app.schemas.health import Health

router = APIRouter()


@router.get("/health", response_description="The API is reachable")
async def get_health() -> Health:
    return Health(status="ok")
