# syntax = docker/dockerfile:1

FROM node:18.14.2-slim AS base

ARG PORT=3000
ENV PORT=$PORT
ENV NODE_ENV=production

WORKDIR /app

# Dependencies Installation
FROM base AS dependencies
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile --production=false

# Build Stage
FROM dependencies AS build
COPY . .
RUN yarn build
RUN yarn install --production --ignore-scripts --prefer-offline

# Production Image
FROM base AS production

# Kopiere notwendige Dateien
COPY --from=build /app/.output /app/.output
COPY --from=build /app/node_modules /app/node_modules
COPY .env /app/.env

# Exponiere den Port
EXPOSE $PORT

# Starte die Anwendung
CMD [ "node", ".output/server/index.mjs" ]