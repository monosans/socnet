#!/usr/bin/env bash

set -euo pipefail

python3 /app/manage.py migrate --noinput
python3 /app/manage.py collectstatic --noinput --clear
python3 /app/manage.py compilemessages --locale en --locale ru
exec gunicorn --config python:docker.django.gunicorn_config config.asgi:application
