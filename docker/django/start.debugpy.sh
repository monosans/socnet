#!/usr/bin/env bash

set -euo pipefail

exec python3 -m debugpy --wait-for-client --listen 0.0.0.0:5678 uvicorn --host 0.0.0.0 --reload --reload-include '*.html' --log-config config/settings/logging.json --no-server-header config.asgi:application
