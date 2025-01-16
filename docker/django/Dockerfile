# syntax=docker/dockerfile:1

FROM docker.io/node:lts-bookworm-slim AS node-base-stage

WORKDIR /app

COPY ./package.json ./

RUN --mount=type=cache,target=/root/.npm \
  --mount=source=package-lock.json,target=package-lock.json \
  npm ci


FROM node-base-stage AS node-build-stage

RUN --mount=source=tsconfig.json,target=tsconfig.json \
  --mount=source=socnet/static/private,target=socnet/static/private \
  npm run build


FROM node-base-stage AS node-watch-stage

USER node

CMD ["npm", "run", "watch"]


FROM docker.io/python:3.13-slim-bookworm AS python-base-stage

ENV \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app


FROM python-base-stage AS python-build-stage

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

ENV \
  PATH="/root/.cargo/bin:${PATH}" \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy

COPY ./socnet_rs/ ./socnet_rs/

ARG EXTRA

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
  --mount=type=cache,target=/app/socnet_rs/target,sharing=locked \
  --mount=type=cache,target=/root/.cache/uv,sharing=locked \
  --mount=type=cache,target=/root/.cargo/registry,sharing=locked \
  --mount=source=pyproject.toml,target=pyproject.toml \
  --mount=source=uv.lock,target=uv.lock \
  uv sync --extra="${EXTRA}" --no-dev --no-install-project --frozen


FROM python-base-stage AS python-ci-run-stage

ENV DJANGO_SETTINGS_MODULE=config.settings.local

RUN apt-get update \
  && apt-get install -y --no-install-recommends gettext wait-for-it \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage --link /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["bash", "/app/docker/django/entrypoint.sh"]

CMD ["bash", "/app/docker/django/start.sh"]


FROM python-base-stage AS python-local-run-stage

ENV DJANGO_SETTINGS_MODULE=config.settings.local

RUN apt-get update \
  && apt-get install -y --no-install-recommends gettext wait-for-it \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && groupadd --gid 1000 django \
  && useradd --gid 1000 --no-log-init --uid 1000 django

COPY --from=python-build-stage --chown=1000:1000 --link /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

USER django

ENTRYPOINT ["bash", "/app/docker/django/entrypoint.sh"]

CMD ["bash", "/app/docker/django/start.sh"]


FROM python-base-stage AS python-production-run-stage

ENV DJANGO_SETTINGS_MODULE=config.settings.production

RUN apt-get update \
  && apt-get install -y --no-install-recommends gettext libpq-dev wait-for-it \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && groupadd --gid 1000 django \
  && useradd --gid 1000 --no-log-init --uid 1000 django \
  && mkdir -p /var/www/django/static /var/www/django/media \
  && chown 1000:1000 /var/www/django/static /var/www/django/media

COPY --from=python-build-stage --chown=1000:1000 --link /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY --chown=1000:1000 . .
COPY --from=node-build-stage --chown=1000:1000 --link /app/socnet/static/public/css/ /app/socnet/static/public/css/
COPY --from=node-build-stage --chown=1000:1000 --link /app/socnet/static/public/js/ /app/socnet/static/public/js/

USER django

ENTRYPOINT ["bash", "/app/docker/django/entrypoint.prod.sh"]

CMD ["bash", "/app/docker/django/start.prod.sh"]
