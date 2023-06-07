#!/usr/bin/env bash

set -euo pipefail

while ! </dev/tcp/"${POSTGRES_HOST}"/"${POSTGRES_PORT}"; do sleep 1; done

exec "$@"
