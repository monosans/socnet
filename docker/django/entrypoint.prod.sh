#!/usr/bin/env bash

set -euo pipefail

while ! </dev/tcp/postgres/5432; do sleep 1; done
while ! </dev/tcp/redis/6379; do sleep 1; done

exec "$@"
