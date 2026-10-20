FROM node:24-slim AS build
RUN corepack enable
WORKDIR /app/frontend
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY backend/openapi.json /app/backend/openapi.json
COPY frontend ./
RUN pnpm exec openapi-ts && pnpm run build

FROM nginxinc/nginx-unprivileged:1.30-alpine
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/frontend/dist /usr/share/nginx/html
EXPOSE 8080
