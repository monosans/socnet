# syntax=docker.io/docker/dockerfile:1

FROM docker.io/node:lts-bookworm-slim AS node-base

WORKDIR /app

COPY --link ./package.json ./

RUN --mount=type=cache,target=/root/.npm,sharing=locked \
  --mount=source=package-lock.json,target=package-lock.json \
  npm ci


FROM node-base AS node-build

RUN --mount=source=tsconfig.json,target=tsconfig.json \
  --mount=source=socnet/static/private,target=socnet/static/private \
  npm run build


FROM node-base AS node-watch

ARG \
  UID=1000 \
  GID=1000

RUN groupmod --gid "${GID}" node \
  && usermod --uid "${UID}" --gid "${GID}" node

USER node

CMD ["npm", "run", "watch"]


FROM docker.io/python:3.13-slim-bookworm AS python-base

ENV \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app

RUN rm -f /etc/apt/apt.conf.d/docker-clean \
  && echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache


FROM python-base AS python-builder

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && curl -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain beta --profile minimal

ENV \
  PATH="/root/.cargo/bin:${PATH}" \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy \
  UV_PYTHON_DOWNLOADS=0

COPY --link ./socnet_rs/ ./socnet_rs/

ARG EXTRA

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
  --mount=type=cache,target=/app/socnet_rs/target,sharing=locked \
  --mount=type=cache,target=/root/.cache/uv,sharing=locked \
  --mount=type=cache,target=/root/.cargo/registry,sharing=locked \
  --mount=source=pyproject.toml,target=pyproject.toml \
  --mount=source=uv.lock,target=uv.lock \
  uv sync --extra="${EXTRA}" --no-dev --no-install-project --locked


FROM python-base AS python-ci

ENV DJANGO_SETTINGS_MODULE=config.settings.local

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update \
  && apt-get install -y --no-install-recommends gettext wait-for-it

COPY --from=python-builder --link /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["bash", "/app/docker/django/entrypoint.sh"]

CMD ["bash", "/app/docker/django/start.sh"]


FROM python-base AS python-local

ENV DJANGO_SETTINGS_MODULE=config.settings.local

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update \
  && apt-get install -y --no-install-recommends gettext wait-for-it

ARG \
  UID=1000 \
  GID=1000

RUN (getent group "${GID}" || groupadd --gid "${GID}" django) \
  && useradd --gid "${GID}" --no-log-init --uid "${UID}" django

COPY --from=python-builder --chown=${UID}:${GID} --link /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

USER django

ENTRYPOINT ["bash", "/app/docker/django/entrypoint.sh"]

CMD ["bash", "/app/docker/django/start.sh"]


FROM python-base AS python-production

ENV DJANGO_SETTINGS_MODULE=config.settings.production

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update \
  && apt-get install -y --no-install-recommends gettext libpq-dev wait-for-it \
  && groupadd --gid 1000 django \
  && useradd --gid 1000 --no-log-init --uid 1000 django \
  && mkdir -p /var/www/django/static /var/www/django/media \
  && chown 1000:1000 /var/www/django/static /var/www/django/media

COPY --from=python-builder --chown=1000:1000 --link /app/.venv /app/.venv
COPY --from=node-build --chown=1000:1000 --link /app/socnet/static/public/css/ /app/socnet/static/public/css/
COPY --from=node-build --chown=1000:1000 --link /app/socnet/static/public/js/ /app/socnet/static/public/js/

ENV PATH="/app/.venv/bin:$PATH"

USER django

COPY --chown=1000:1000 --link . .

ENTRYPOINT ["bash", "/app/docker/django/entrypoint.prod.sh"]

CMD ["bash", "/app/docker/django/start.prod.sh"]
