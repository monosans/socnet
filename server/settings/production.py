from .base import *

ALLOWED_HOSTS = [env("DOMAIN_NAME")]

DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

_REDIS_HOST = env("REDIS_HOST")
_REDIS_PORT = env.int("REDIS_PORT")
_REDIS_URL = f"redis://{_REDIS_HOST}:{_REDIS_PORT}"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{_REDIS_URL}/1",
    }
}

CHANNEL_LAYERS["default"] = {
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    "CONFIG": {"hosts": [f"{_REDIS_URL}/2"]},
}

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")

STATIC_ROOT = "/var/www/django/static"
MEDIA_ROOT = "/var/www/django/media"
