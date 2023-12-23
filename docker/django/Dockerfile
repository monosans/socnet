FROM node:lts-bookworm-slim as node

WORKDIR /app

COPY ./package.json ./package-lock.json ./

RUN npm ci && \
  npm cache clean --force


FROM node as node-esbuild

COPY ./tsconfig.json ./tsconfig.json
COPY ./socnet/static/private/css/ ./socnet/static/private/css/
COPY ./socnet/static/private/js/ ./socnet/static/private/js/

RUN npm run build


FROM python:3.12-slim-bookworm as python

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

WORKDIR /app


FROM python as python-build-stage

# hadolint ignore=DL3008,DL3013,DL4006
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev pkg-config \
  && curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && pip install \
  --progress-bar off \
  --no-cache-dir \
  --disable-pip-version-check \
  --no-color \
  poetry poetry-plugin-export

ENV PATH="/root/.cargo/bin:${PATH}"

COPY ./poetry.lock ./pyproject.toml ./
COPY ./socnet_rs/ ./socnet_rs/

ARG POETRY_GROUPS

# hadolint ignore=DL4006
RUN poetry export \
  --without-hashes \
  --without-urls \
  --only="${POETRY_GROUPS}" \
  --no-ansi \
  --no-interaction \
  --no-cache | \
  pip wheel \
  --wheel-dir /usr/src/app/wheels \
  -r /dev/stdin \
  --progress-bar off \
  --no-deps \
  --no-cache-dir \
  --disable-pip-version-check \
  --no-color


FROM python as python-ci-run-stage

# hadolint ignore=DL3008
RUN apt-get update \
  && apt-get install -y --no-install-recommends gettext libpq-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels/ /wheels/

RUN pip install \
  --progress-bar off \
  --no-index \
  --find-links /wheels/ /wheels/* \
  --no-cache-dir \
  --disable-pip-version-check \
  --no-color \
  && rm -rf /wheels/

ENTRYPOINT ["bash", "/app/docker/django/entrypoint.sh"]


FROM python-ci-run-stage as python-local-run-stage

ARG UID GID

RUN groupadd --gid "${GID}" --system django \
  && useradd --gid django --no-log-init --system --uid "${UID}" django

USER django


FROM python as python-production-run-stage

# hadolint ignore=DL3008
RUN apt-get update \
  && apt-get install --no-install-recommends -y brotli gettext libpq-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && groupadd --system django \
  && useradd --gid django --system django \
  && mkdir -p /var/www/django/static /var/www/django/media \
  && chown django:django /var/www/django/static /var/www/django/media

COPY --from=python-build-stage /usr/src/app/wheels/ /wheels/

RUN pip install \
  --progress-bar off \
  --no-index \
  --find-links /wheels/ /wheels/* \
  --no-cache-dir \
  --disable-pip-version-check \
  --no-color \
  && rm -rf /wheels/

COPY --chown=django:django . .
COPY --chown=django:django --from=node-esbuild /app/socnet/static/public/css/ /app/socnet/static/public/css/
COPY --chown=django:django --from=node-esbuild /app/socnet/static/public/js/ /app/socnet/static/public/js/

USER django

ENTRYPOINT ["bash", "/app/docker/django/entrypoint.prod.sh"]
