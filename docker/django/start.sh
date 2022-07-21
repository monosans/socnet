#!/usr/bin/env bash

set -euo pipefail

python3 /app/manage.py migrate --noinput
python3 /app/manage.py collectstatic --noinput --clear
python3 /app/manage.py compilemessages

find /var/www/django/static -type f \
	! -regex '^.+\.\(jpg\|jpeg\|png\|gif\|webp\|zip\|gz\|tgz\|bz2\|tbz\|xz\|br\|swf\|flv\|woff\|woff2\)$' \
	-exec brotli --force --best {} \+ \
	-exec gzip --force --keep --best {} \+

/usr/local/bin/gunicorn --config python:docker.django.gunicorn_config server.asgi:application
