# hadolint global ignore=DL3008,DL3013,DL4006
FROM docker.io/node:lts-bookworm-slim as node-base-stage

WORKDIR /app

COPY ./package.json ./package-lock.json ./

RUN npm ci && \
  npm cache clean --force


FROM node-base-stage as node-build-stage

COPY ./tsconfig.json ./tsconfig.json
COPY ./socnet/static/private/css/ ./socnet/static/private/css/
COPY ./socnet/static/private/js/ ./socnet/static/private/js/

RUN npm run build


FROM node-base-stage as node-watch-stage

RUN apt-get update \
  && apt-get install -y --no-install-recommends tini \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

ARG GID UID

RUN groupmod --gid "${GID}" node \
  && usermod --gid node --uid "${UID}" node

USER node

ENTRYPOINT ["tini", "--"]

CMD ["npm", "run", "watch"]


FROM docker.io/python:3.12-slim-bookworm as python-base-stage

ENV \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_COLOR=1 \
  PIP_NO_INPUT=1 \
  PIP_PROGRESS_BAR=off \
  PIP_ROOT_USER_ACTION=ignore \
  PIP_UPGRADE=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app


FROM python-base-stage as python-build-stage

ENV \
  POETRY_NO_ANSI=1 \
  POETRY_NO_CACHE=1 \
  POETRY_NO_INTERACTION=1

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.cargo/bin:${PATH}"

RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
  pip install poetry poetry-plugin-export

COPY ./poetry.lock ./pyproject.toml ./
COPY ./socnet_rs/ ./socnet_rs/

ARG POETRY_GROUPS

RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
  poetry export --without-hashes --only="${POETRY_GROUPS}" | \
  pip wheel --wheel-dir /usr/src/app/wheels -r /dev/stdin


FROM python-base-stage as python-base-run-stage

ENV READ_ENV_EXAMPLE=False


FROM python-base-run-stage as python-ci-run-stage

ENV DJANGO_SETTINGS_MODULE=config.settings.local

RUN apt-get update \
  && apt-get install -y --no-install-recommends gettext libpq-dev tini wait-for-it \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels/ /wheels/

RUN pip install --no-index --find-links /wheels/ /wheels/* \
  && rm -rf /wheels/

ENTRYPOINT ["tini", "--", "/app/docker/django/entrypoint.sh"]

CMD ["/app/docker/django/start.sh"]


FROM python-ci-run-stage as python-local-run-stage

ARG GID UID

RUN groupadd --gid "${GID}" --system django \
  && useradd --gid django --no-log-init --system --uid "${UID}" django

USER django


FROM python-base-run-stage as python-production-run-stage

ENV DJANGO_SETTINGS_MODULE=config.settings.production

RUN apt-get update \
  && apt-get install -y --no-install-recommends brotli gettext libpq-dev tini wait-for-it \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && groupadd --system django \
  && useradd --gid django --no-log-init --system django \
  && mkdir -p /var/www/django/static /var/www/django/media \
  && chown django:django /var/www/django/static /var/www/django/media

COPY --from=python-build-stage /usr/src/app/wheels/ /wheels/

RUN pip install --no-index --find-links /wheels/ /wheels/* \
  && rm -rf /wheels/

COPY . .
COPY --from=node-build-stage /app/socnet/static/public/css/ /app/socnet/static/public/css/
COPY --from=node-build-stage /app/socnet/static/public/js/ /app/socnet/static/public/js/

USER django

ENTRYPOINT ["tini", "--", "/app/docker/django/entrypoint.prod.sh"]

CMD ["/app/docker/django/start.prod.sh"]
