#!/usr/bin/env bash

set -euo pipefail

python3 /app/manage.py collectstatic --noinput --clear
python3 /app/manage.py compilemessages --locale en --locale ru
exec gunicorn --config python:config.settings.gunicorn config.asgi:application
