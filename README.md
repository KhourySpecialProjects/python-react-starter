# Python React Starter

A starting point for a web app with a React frontend, a FastAPI backend and a
Postgres database. Docker Compose runs all three. [mise](https://mise.jdx.dev)
installs the tools and runs every command.

```
browser ──> web (React + Vite, :5173) ──/api/v1──> backend (FastAPI, :8000) ──> postgres (:5432)
```

## Quickstart

You need [Docker](https://docs.docker.com/get-docker/) and
[mise](https://mise.jdx.dev/getting-started.html).

```sh
cp .env.example .env   # local settings; the defaults work
mise install           # installs the pinned Node, pnpm, Python, uv and ruff
mise run install       # installs packages on your machine, for your editor and checks
mise run dev           # starts postgres, backend and web with hot reload
```

Open http://localhost:5173 and click **Load notes**. The first migration
creates the `notes` table with a few example rows, so you'll see them right away.

The API docs are at http://localhost:8000/api/v1/docs.

## Layout

```
backend/
  src/app/
    main.py              creates the FastAPI app, middleware and routers
    routes/              HTTP handlers, one file per resource, all under /api/v1
    models/              SQLAlchemy tables, one file per table
    schemas/             pydantic request and response models, one file per resource
    core/
      settings.py        environment variables
      db.py              async engine and the SessionDep dependency
      http_client.py     shared httpx client (HttpClientDep) for calling other services
      logging_config.py  log format (text locally, JSON when deployed) and request ids
      middleware.py      logs one line per request
  migrations/            Alembic migrations
  openapi.json           the API contract, generated from the routes
frontend/
  src/App.tsx            the page layout
  src/components/        React components, one per file
  src/client/            typed API client, generated from backend/openapi.json
  nginx.conf             web server for deployed environments
compose.yaml             the deployed stack
compose.override.yaml    local settings, merged on top of compose.yaml
mise.toml                tool versions and every task
AGENTS.md                rules for humans and coding agents; .agents/rules has more
```

## Tasks

Run `mise tasks` for the full list.

| Task | What it does |
| --- | --- |
| `mise run dev` | Start everything with hot reload |
| `mise run down` | Stop everything (database data is kept) |
| `mise run logs [service]` | Tail logs |
| `mise run check` | Run every check CI runs: format, lint, typecheck, and a stale-client check |
| `mise run fmt:fix` / `lint:fix` | Fix formatting and lint issues |
| `mise run client:generate` | Export the API contract and regenerate the frontend client |
| `mise run db:revision "add users"` | Generate a migration from changes to `models/` |
| `mise run db:migrate` | Apply migrations (the backend also does this on start) |
| `mise run db:rollback` | Undo the latest migration |
| `mise run db:psql` | Open a SQL shell |
| `mise run db:reset` | Delete the local database and start fresh |
| `mise run deploy:check` | Build the deployed stack and check that every container is healthy |

## How the frontend talks to the backend

The backend's routes and pydantic models are the contract. When you change one:

1. `mise run client:generate` writes `backend/openapi.json` and regenerates
   `frontend/src/client`.
2. The frontend calls the new function, e.g. `listNotes()`. It is fully typed,
   so `tsc` catches a field the backend renamed or removed.
3. Commit both. CI fails if either one is out of date
   (`mise run contract:check` and `mise run client:check`).

The frontend always calls relative URLs like `/api/v1/notes`. Locally, Vite
forwards `/api` to the backend container. When deployed, nginx does the same.
The browser only ever sees one origin, so there is no CORS to configure.

## Changing the database

The models in `backend/src/app/models/` are the source of truth for the
schema. To add a table or column, or change one:

1. Edit a model, or add a new file like `models/user.py` and import it in
   `models/__init__.py`. Alembic can't see a model that isn't imported there.
2. `mise run db:revision "add <table>"`. Alembic compares your models with the
   database and writes a migration to `backend/migrations/versions/`. Read it
   before committing. If nothing changed, it writes nothing.
3. `mise run db:migrate`, or restart the backend.

## Make it yours

Rename the project:

- `name:` in `compose.yaml`, and the `-p python-react-starter-deploy` project
  name in the `deploy:check` task in `mise.toml`
- `name` and `description` in `backend/pyproject.toml`, then run
  `uv lock --directory backend`
- `title` in `backend/src/app/main.py`
- `name` in `frontend/package.json`
- `<title>` in `frontend/index.html` and the heading in `frontend/src/App.tsx`
- this README

Remove the notes example once you have your own feature:

- delete `backend/src/app/routes/notes.py` and its lines in `routes/__init__.py`
- delete `models/note.py` (and its import in `models/__init__.py`) and
  `schemas/note.py`
- run `mise run db:revision "drop notes"` to generate a migration that drops
  the table
- run `mise run client:generate`, delete `frontend/src/components/NoteList.tsx`
  and remove it from `App.tsx`

## Deploying

`compose.yaml` is the deployed stack, and it works as-is on platforms that read
a Compose file, such as Coolify. It builds the `deploy` stage of each
Dockerfile:

- `backend` applies migrations, then runs uvicorn without reload, as a non-root
  user, with JSON logs.
- `web` builds the frontend into static files and serves them with nginx
  (`frontend/nginx.conf`). nginx forwards `/api/` to the backend, falls back to
  `index.html` for client-side routes, caches `/assets/` for a year, and logs
  each request as JSON.

Run `mise run deploy:check` before your first deploy to build that stack
locally and check that it comes up healthy.

## Troubleshooting

- **Port already in use.** Another app is using 5173, 8000 or 5432. For
  Postgres, set `POSTGRES_PORT` in `.env` and change the port in
  `DATABASE_URL` to match. For the others, change the left side of the port in
  `compose.override.yaml`.
- **`not set. Create your .env file`.** Run `cp .env.example .env`.
- **The frontend can't find a package you just added.** The container has its
  own `node_modules`. Run `docker compose restart web`, which reinstalls on
  start. The same goes for `backend` after adding a Python package.
