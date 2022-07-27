#!/usr/bin/env bash

set -euo pipefail

python3 <<END
import sys
import time

import psycopg2

while True:
    try:
        psycopg2.connect(
            dbname="${POSTGRES_DB}",
            user="${POSTGRES_USER}",
            password="${POSTGRES_PASSWORD}",
            host="${POSTGRES_HOST}",
            port="${POSTGRES_PORT}",
        )
    except psycopg2.OperationalError as e:
        sys.stderr.write(str(e))
    else:
        break
    time.sleep(1)
END

exec "$@"
