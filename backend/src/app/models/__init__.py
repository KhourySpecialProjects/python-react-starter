# Import every model here. Alembic only sees tables whose model has been
# imported, so a model missing from this list gets no migration.
from app.models.base import Base
from app.models.note import Note

__all__ = ["Base", "Note"]
