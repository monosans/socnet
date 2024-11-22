#!/usr/bin/env bash

set -euo pipefail

python3 /app/manage.py compilemessages --locale en --locale ru
exec python3 -m debugpy --wait-for-client --listen 0.0.0.0:5678 python3 /app/dev_serve.py
