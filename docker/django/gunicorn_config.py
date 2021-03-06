"""https://docs.gunicorn.org/en/stable/settings.html"""
from __future__ import annotations

import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1

# https://adamj.eu/tech/2019/09/19/working-around-memory-leaks-in-your-django-app/
max_requests = 1000
max_requests_jitter = 100

chdir = "/app"
worker_tmp_dir = "/dev/shm"
worker_class = "uvicorn.workers.UvicornWorker"
