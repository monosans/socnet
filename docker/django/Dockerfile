FROM python:3-slim as python

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

FROM python as python-build-stage

ARG BUILD_ENVIRONMENT

# hadolint ignore=DL3008
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  # required for building Python packages
  build-essential \
  # required for psycopg2
  libpq-dev

# Copy requirements to cache them
COPY ./requirements .

# Create wheels
RUN pip wheel --progress-bar off --no-color --wheel-dir /usr/src/app/wheels \
  -r "${BUILD_ENVIRONMENT}".txt

FROM python as python-local-stage

ARG BUILD_ENVIRONMENT \
  UID \
  GID

# hadolint ignore=DL3008
RUN groupadd -g "${GID}" -r django \
  && useradd -g django -l -r -u "${UID}" django \
  && if [ "${BUILD_ENVIRONMENT}" = 'production' ]; \
  then mkdir -p /var/www/django/static /var/www/django/media \
  && chown django:django /var/www/django/static /var/www/django/media; fi \
  && apt-get update \
  && apt-get install --no-install-recommends -y \
  # static files compression
  brotli \
  # required for psycopg2
  libpq-dev \
  # i18n
  gettext \
  # cleaning up
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

# Copy wheels from build-stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Install wheels
RUN pip install --no-cache-dir --no-index --progress-bar off --no-color \
  --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

COPY --chown=django:django ./docker/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER django

ENTRYPOINT ["/entrypoint.sh"]

FROM python-local-stage AS python-production-stage

COPY --chown=django:django ./docker/django/start.sh /start.sh
RUN chmod +x /start.sh

COPY --chown=django:django . .
