# syntax=docker/dockerfile:1

# Node and pnpm versions are pinned here and in mise.toml. Keep them in sync.
FROM node:24.22.0-alpine AS base
RUN npm install --global pnpm@12.14.0
WORKDIR /app

# ---------------------------------------------------------------------------
# local: your laptop only, selected by compose.override.yaml. Source code comes
# from the bind mount; node_modules is a separate volume so it never clashes
# with the one on your machine. Installs packages, then runs the Vite dev
# server (hot reload).
# ---------------------------------------------------------------------------
FROM base AS local
EXPOSE 5173
CMD ["sh", "-c", "pnpm install --frozen-lockfile && exec pnpm exec vite"]

# ---------------------------------------------------------------------------
# build: type-check and bundle the app into static files in dist/
# ---------------------------------------------------------------------------
FROM base AS build
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build

# ---------------------------------------------------------------------------
# deploy: every deployed environment, selected by compose.yaml. nginx serves
# the static files and forwards /api requests to the backend container. Runs
# as a non-root user, so it listens on 8080 instead of 80.
# ---------------------------------------------------------------------------
FROM nginxinc/nginx-unprivileged:1.30.6-alpine AS deploy
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
