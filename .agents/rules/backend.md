---
paths:
  - "backend/**"
---

# Backend rules

FastAPI, SQLAlchemy and Alembic rules for `backend/`, on top of the root
`AGENTS.md`. Copy the shape of the notes example for a new resource:
`models/note.py`, `schemas/note.py`, `routes/notes.py`.

## Where code goes

- `routes/`: HTTP handlers. One file per resource, added to `api_router` in
  `routes/__init__.py`. Every route lives under `/api/v1`.
- `models/`: SQLAlchemy tables, one file per table. Import each one in
  `models/__init__.py`, or Alembic will not see it.
- `schemas/`: pydantic request and response models, one file per resource.
- `core/`: app-wide setup (settings, database, logging, middleware, HTTP
  client). Feature code does not go here.

## Rules

- Routes are `async def` and use `SessionDep` for the database. A blocking
  call (sync DB driver, `requests`, `time.sleep`) stalls every other request,
  including `/api/v1/health`. Use `HttpClientDep` to call other services.
- Every route declares a pydantic response model as its return type. Never
  return a SQLAlchemy model or a bare `dict`.
- Change the schema only by editing models, then run
  `mise run db:revision "what changed"`. Read the generated file before
  committing it. Never edit a migration that is already on `main`.
- End every `ORDER BY` with a unique column, usually `id`, so rows come back in
  the same order every time.
- Log with `logging.getLogger(__name__)`. Routine success is `debug`. Do not
  log passwords, tokens or full request bodies.
- New environment variables go in `core/settings.py` and `.env.example`.
- Code must pass `mypy --strict`. Avoid `Any` and `# type: ignore`. If you need
  one, add a comment saying why.
