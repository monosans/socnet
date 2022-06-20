#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

echo "DJANGO_ENV is $DJANGO_ENV"
if [ "$DJANGO_ENV" != 'production' ]; then
  echo 'Error: DJANGO_ENV is not set to "production".'
  echo 'Application will not start.'
  exit 1
fi

export DJANGO_ENV

python /code/manage.py migrate --noinput
python /code/manage.py collectstatic --noinput
python /code/manage.py compilemessages

# http://docs.gunicorn.org/en/stable/settings.html
/usr/local/bin/gunicorn \
  --config python:docker.django.gunicorn_config \
  server.asgi:application
