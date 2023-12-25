#!/usr/bin/env bash

set -euo pipefail

wait-for-it "${POSTGRES_HOST}:${POSTGRES_PORT}"

exec "$@"
