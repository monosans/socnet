#!/usr/bin/env bash

set -euo pipefail

exec uvicorn --host 0.0.0.0 --reload --reload-include '*.html' --log-config config/settings/logging.json --no-server-header config.asgi:application
