"""https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/"""
from .config import config

DEBUG = False

ALLOWED_HOSTS = [config("DOMAIN_NAME")]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000  # the same as Caddy has
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

DEFENDER_BEHIND_REVERSE_PROXY = True

STATIC_ROOT = "/var/www/django/static"
MEDIA_ROOT = "/var/www/django/media"
