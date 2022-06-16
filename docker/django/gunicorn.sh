#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

# Check that $DJANGO_ENV is set to "production",
# fail otherwise, since it may break things:
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

# Start gunicorn:
# Docs: http://docs.gunicorn.org/en/stable/settings.html
# Concerning `workers` setting see:
# https://adamj.eu/tech/2019/09/19/working-around-memory-leaks-in-your-django-app/
/usr/local/bin/gunicorn server.asgi:application \
  --workers=$(nproc --all) \
  --max-requests=2000 \
  --max-requests-jitter=400 \
  --bind='0.0.0.0:8000' \
  --chdir='/code' \
  --log-file=- \
  --worker-tmp-dir='/dev/shm' \
  --worker-class 'uvicorn.workers.UvicornWorker'
