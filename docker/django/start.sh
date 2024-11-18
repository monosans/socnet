#!/usr/bin/env bash

set -euo pipefail

python3 /app/manage.py compilemessages --locale en --locale ru
exec python3 /app/run.py
