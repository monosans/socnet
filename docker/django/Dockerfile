# hadolint global ignore=DL3008,DL3013,DL3042,DL4006,SC3028
FROM docker.io/node:lts-bookworm-slim AS node-base-stage

WORKDIR /app

COPY ./package.json ./

RUN --mount=type=cache,target=/root/.npm \
  --mount=type=bind,source=package-lock.json,target=package-lock.json \
  npm ci


FROM node-base-stage AS node-build-stage

RUN --mount=type=bind,source=tsconfig.json,target=tsconfig.json \
  --mount=type=bind,source=socnet/static/private,target=socnet/static/private \
  npm run build


FROM node-base-stage AS node-watch-stage

RUN apt-get update \
  && apt-get install -y --no-install-recommends tini \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

USER node

ENTRYPOINT ["tini", "--"]

CMD ["npm", "run", "watch"]


FROM docker.io/python:3.12-slim-bookworm AS python-base-stage

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
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  uv sync --extra="${EXTRA}" --no-dev --no-install-project --frozen


FROM python-base-stage AS python-base-run-stage

ENV READ_ENV_EXAMPLE=False


FROM python-base-run-stage AS python-ci-run-stage

ENV DJANGO_SETTINGS_MODULE=config.settings.local

RUN apt-get update \
  && apt-get install -y --no-install-recommends gettext tini wait-for-it \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["tini", "--", "bash", "/app/docker/django/entrypoint.sh"]

CMD ["bash", "/app/docker/django/start.sh"]


FROM python-base-run-stage AS python-local-run-stage

ENV DJANGO_SETTINGS_MODULE=config.settings.local

RUN apt-get update \
  && apt-get install -y --no-install-recommends gettext tini wait-for-it \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && groupadd --gid 1000 django \
  && useradd --gid 1000 --no-log-init --uid 1000 django

COPY --chown=django:django --from=python-build-stage /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

USER django

ENTRYPOINT ["tini", "--", "bash", "/app/docker/django/entrypoint.sh"]

CMD ["bash", "/app/docker/django/start.sh"]


FROM python-base-run-stage AS python-production-run-stage

ENV DJANGO_SETTINGS_MODULE=config.settings.production

RUN apt-get update \
  && apt-get install -y --no-install-recommends gettext libpq-dev tini wait-for-it \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && groupadd --gid 1000 django \
  && useradd --gid 1000 --no-log-init --uid 1000 django \
  && mkdir -p /var/www/django/static /var/www/django/media \
  && chown django:django /var/www/django/static /var/www/django/media

COPY --chown=django:django --from=python-build-stage /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY --chown=django:django . .
COPY --chown=django:django --from=node-build-stage /app/socnet/static/public/css/ /app/socnet/static/public/css/
COPY --chown=django:django --from=node-build-stage /app/socnet/static/public/js/ /app/socnet/static/public/js/

USER django

ENTRYPOINT ["tini", "--", "bash", "/app/docker/django/entrypoint.prod.sh"]

CMD ["bash", "/app/docker/django/start.prod.sh"]
