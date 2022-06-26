#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly cmd="$*"

: "${DJANGO_DATABASE_HOST:=db}"
: "${DJANGO_DATABASE_PORT:=5432}"
: "${DJANGO_REDIS_HOST:=redis}"
: "${DJANGO_REDIS_PORT:=6379}"

# Make sure that this container is started
# after the ones with Postgres and Redis:
dockerize \
  -wait "tcp://${DJANGO_DATABASE_HOST}:${DJANGO_DATABASE_PORT}" \
  -wait "tcp://${DJANGO_REDIS_HOST}:${DJANGO_REDIS_PORT}" \
  -timeout 90s

# Evaluating passed command
exec $cmd
