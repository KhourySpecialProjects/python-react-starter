---
paths:
  - "backend/**"
---

# Backend

FastAPI, pydantic and SQLAlchemy. Copy the shape of the messages example for a new
resource: `models/message.py`, `schemas/message.py`, `routes/messages.py`.

## Where code goes

- `main.py`: creates the app and wires in middleware and routers. Run it with
  `python -m app.main`.
- `routes/`: HTTP handlers, one file per resource, added to `api_router` in
  `routes/__init__.py`. Every route lives under `/api/v1`.
- `models/`: SQLAlchemy tables, one file per table, imported in `models/__init__.py`.
- `schemas/`: pydantic request and response models, one file per resource.
- `middleware/`: request middleware.
- `config/`: settings, the database session and logging.

## Rules

- Routes are `async def` and use `SessionDep` for the database. Call other services
  with `httpx.AsyncClient`, never `requests`.
- The handler's name becomes the operationId in camelCase, so `list_messages` becomes
  `listMessages()` in the frontend. Name handlers after what they do.
- Every route declares a pydantic response model as its return type. Never return a
  SQLAlchemy model or a bare `dict`. Schemas use camelCase aliases in JSON.
- Query with `select()` / `insert()` / `update()` / `delete()` or `text()` only. See
  "Queries" in `AGENTS.md`.
- Change tables only through `models/` and `mise run db:dev:migrate:generate <name>`.
- End every `ORDER BY` with a unique column, usually `id`.
- Log with `logging.getLogger(__name__)`. Never `print`.
- New environment variables go in `config/settings.py` and `.env.example`.
- Code must pass `mypy --strict`. Avoid `Any` and `# type: ignore`.
