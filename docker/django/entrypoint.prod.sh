#!/usr/bin/env bash

set -euo pipefail

wait-for-it "${POSTGRES_HOST}:${POSTGRES_PORT}"
wait-for-it "${REDIS_HOST}:${REDIS_PORT}"

exec "$@"
