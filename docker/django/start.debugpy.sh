#!/usr/bin/env bash

set -euo pipefail

exec python3 -m debugpy --wait-for-client --listen 0.0.0.0:5678 python3 /app/run.py
