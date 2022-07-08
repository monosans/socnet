#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

python3 /app/manage.py migrate --noinput
python3 /app/manage.py collectstatic --noinput --clear
python3 /app/manage.py compilemessages

/usr/local/bin/gunicorn --config python:docker.django.gunicorn_config server.asgi:application
