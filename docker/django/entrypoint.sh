#!/usr/bin/env bash

set -euo pipefail

postgres_ready() {
	python3 <<END
import psycopg2

try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
except psycopg2.OperationalError:
    raise SystemExit(-1)
raise SystemExit
END
}

until postgres_ready; do
	echo >&2 'Waiting for PostgreSQL to become available...'
	sleep 1
done

exec "$@"
