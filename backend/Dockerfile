# Python and uv versions are pinned here and in mise.toml. Keep them in sync.
FROM python:3.14.8-slim AS base
COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /usr/local/bin/uv
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    PYTHONUNBUFFERED=1

FROM base AS build
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project
COPY src src
RUN uv sync --locked --no-dev --no-editable

FROM base AS deploy
COPY --from=ghcr.io/amacneil/dbmate:2.37.0 /usr/local/bin/dbmate /usr/local/bin/dbmate
RUN useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin app
COPY --from=build /opt/venv /opt/venv
COPY migrations migrations
USER app
EXPOSE 3000
CMD ["sh", "-c", "dbmate --migrations-dir migrations --no-dump-schema migrate && exec python -m app.main"]
