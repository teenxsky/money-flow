FROM oven/bun:1.2-alpine AS build-stage
WORKDIR /frontend

COPY ./frontend/package.json .
COPY ./frontend/bun.lock .
RUN bun install

COPY ./frontend .
RUN bun run build


FROM node:20.19-alpine AS production-stage

RUN addgroup --system app && adduser --system --ingroup app app
USER app

COPY --from=build-stage /frontend/.output /nuxt
