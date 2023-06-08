#!/usr/bin/env bash

set -euo pipefail

python3 /app/manage.py migrate --noinput
python3 /app/manage.py collectstatic --noinput --clear
python3 /app/manage.py compilemessages

# Compress static files with brotli and gzip
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
	-exec brotli --force --keep --best {} \+ \
	-exec gzip --force --keep --best {} \+

# Delete compressed files if they are not smaller than the original
find /var/www/django/static -type f | while read -r file; do
	if [[ ${file} == *.br || ${file} == *.gz ]]; then
		continue
	fi
	orig_size=$(stat -c %s "${file}")
	for ext in br gz; do
		compr_file="${file}.${ext}"
		if [[ -e ${compr_file} ]]; then
			compr_size=$(stat -c %s "${compr_file}")
			if ((compr_size >= orig_size)); then
				rm "${compr_file}"
			fi
		fi
	done
done

exec /usr/local/bin/gunicorn --config python:docker.django.gunicorn_config config.asgi:application
