#!/usr/bin/env bash

set -euo pipefail

while ! </dev/tcp/postgres/"${POSTGRES_PORT}"; do sleep 1; done

exec "$@"
