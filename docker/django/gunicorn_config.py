# https://docs.gunicorn.org/en/stable/configure.html#configuration-file
# https://docs.gunicorn.org/en/stable/settings.html

import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1

# https://adamj.eu/tech/2019/09/19/working-around-memory-leaks-in-your-django-app/
max_requests = 2000
max_requests_jitter = 400

log_file = "-"
chdir = "/code"
worker_tmp_dir = "/dev/shm"
worker_class = "uvicorn.workers.UvicornWorker"
