# syntax=docker/dockerfile:1

# Python and uv versions are pinned here and in mise.toml. Keep them in sync.
FROM python:3.14.8-slim AS base
COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /usr/local/bin/uv
WORKDIR /app
# The virtualenv lives outside /app so the local bind mount never hides it and
# never clashes with the .venv on your machine.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    PYTHONUNBUFFERED=1

# ---------------------------------------------------------------------------
# local: your laptop only, selected by compose.override.yaml. Source code comes
# from the bind mount. On startup: install packages, apply migrations, then run
# the server with hot reload.
# ---------------------------------------------------------------------------
FROM base AS local
EXPOSE 8000
CMD ["sh", "-c", "uv sync --locked && alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --no-access-log"]

# ---------------------------------------------------------------------------
# build: install runtime dependencies and the app into /opt/venv
# ---------------------------------------------------------------------------
FROM base AS build
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project
COPY src src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

# ---------------------------------------------------------------------------
# deploy: every deployed environment, selected by compose.yaml. Applies
# pending migrations, then starts.
# ---------------------------------------------------------------------------
FROM base AS deploy
RUN useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin app
COPY --from=build /opt/venv /opt/venv
COPY alembic.ini ./
COPY migrations migrations
USER app
EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --no-access-log"]
