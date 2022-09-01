FROM python:3-slim as python

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Required for psycopg2
# hadolint ignore=DL3008
RUN apt-get update \
  && apt-get install --no-install-recommends -y libpq-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


FROM python as python-build-stage

# Required for building Python packages
# hadolint ignore=DL3008
RUN apt-get update \
  && apt-get install --no-install-recommends -y build-essential \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

ARG BUILD_ENVIRONMENT

# Copy requirements to cache them
COPY ./requirements/base.txt ./requirements/"${BUILD_ENVIRONMENT}".txt ./requirements/

# Create wheels
RUN pip wheel \
  -w /usr/src/app/wheels \
  -r ./requirements/"${BUILD_ENVIRONMENT}".txt \
  --progress-bar off \
  --no-cache-dir \
  --disable-pip-version-check \
  --no-color


FROM python as python-base-run-stage

# i18n
# hadolint ignore=DL3008
RUN apt-get update \
  && apt-get install --no-install-recommends -y gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


FROM python-base-run-stage as python-local-run-stage

# Copy wheels from build-stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Install wheels
RUN pip install \
  --progress-bar off \
  --no-index \
  -f /wheels/ /wheels/* \
  --no-cache-dir \
  --no-color \
  && rm -rf /wheels/

ARG UID GID

RUN groupadd -g "${GID}" -r django \
  && useradd -g django -l -r -u "${UID}" django

USER django

ENTRYPOINT ["bash", "/app/docker/django/entrypoint.sh"]


FROM python-base-run-stage as python-production-run-stage

# hadolint ignore=DL3008
RUN apt-get update \
  # Static files compression
  && apt-get install --no-install-recommends -y brotli \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && groupadd -r django \
  && useradd -g django -r django \
  && mkdir -p /var/www/django/static /var/www/django/media \
  && chown django:django /var/www/django/static /var/www/django/media

# Copy wheels from build-stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Install wheels
RUN pip install \
  --progress-bar off \
  --no-index \
  -f /wheels/ /wheels/* \
  --no-cache-dir \
  --no-color \
  && rm -rf /wheels/

COPY --chown=django:django . .

USER django

ENTRYPOINT ["bash", "/app/docker/django/entrypoint.prod.sh"]


FROM python-base-run-stage as python-ci-run-stage

# Copy wheels from build-stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Install wheels
RUN pip install \
  --progress-bar off \
  --no-index \
  -f /wheels/ /wheels/* \
  --no-cache-dir \
  --no-color \
  && rm -rf /wheels/

ENTRYPOINT ["bash", "/app/docker/django/entrypoint.sh"]
