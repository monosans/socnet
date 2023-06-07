#!/usr/bin/env bash

set -euo pipefail

python3 /app/manage.py migrate --noinput
python3 /app/manage.py collectstatic --noinput --clear
python3 /app/manage.py compilemessages

find /var/www/django/static -type f \
	! \( \
	-iname '*.jpg' -o \
	-iname '*.jpeg' -o \
	-iname '*.png' -o \
	-iname '*.gif' -o \
	-iname '*.webp' -o \
	-iname '*.zip' -o \
	-iname '*.gz' -o \
	-iname '*.tgz' -o \
	-iname '*.bz2' -o \
	-iname '*.tbz' -o \
	-iname '*.xz' -o \
	-iname '*.br' -o \
	-iname '*.swf' -o \
	-iname '*.flv' -o \
	-iname '*.woff' -o \
	-iname '*.woff2' -o \
	-iname '*.3gp' -o \
	-iname '*.3gpp' -o \
	-iname '*.asf' -o \
	-iname '*.avi' -o \
	-iname '*.m4v' -o \
	-iname '*.mov' -o \
	-iname '*.mp4' -o \
	-iname '*.mpeg' -o \
	-iname '*.mpg' -o \
	-iname '*.webm' -o \
	-iname '*.wmv' \) \
	-exec brotli --force --best {} \+ \
	-exec gzip --force --keep --best {} \+

exec /usr/local/bin/gunicorn --config python:docker.django.gunicorn_config config.asgi:application
