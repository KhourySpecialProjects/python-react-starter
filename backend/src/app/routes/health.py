from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


# Async and DB-free on purpose: it runs on the event loop, so it answers right
# away even while other requests are waiting on Postgres.
@router.get("/health")
async def get_health() -> HealthResponse:
    return HealthResponse(status="ok")
