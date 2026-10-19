from fastapi import APIRouter
from sqlalchemy import select

from app.core.db import SessionDep
from app.models import Note
from app.schemas.note import NoteResponse

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("")
async def list_notes(session: SessionDep) -> list[NoteResponse]:
    notes = await session.scalars(select(Note).order_by(Note.created_at, Note.id))
    return [NoteResponse.model_validate(note) for note in notes]
