from fastapi import APIRouter
from sqlalchemy import select

from app import models, schemas
from app.config.db import SessionDep

router = APIRouter()


@router.get("/messages", response_description="The 50 most recent messages")
async def list_messages(session: SessionDep) -> list[schemas.Message]:
    rows = await session.scalars(
        select(models.Message)
        .order_by(models.Message.created_at.desc(), models.Message.id.desc())
        .limit(50)
    )
    return [schemas.Message.model_validate(row) for row in rows]
