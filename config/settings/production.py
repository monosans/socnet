from __future__ import annotations

from .base import *

ALLOWED_HOSTS = [env.str("DOMAIN_NAME")]

DATABASES["default"]["CONN_MAX_AGE"] = 60

MIDDLEWARE.remove("socnet.core.middleware.ResponseHeadersMiddleware")

_REDIS_HOST = env.str("REDIS_HOST")
_REDIS_PORT = env.int("REDIS_PORT")
_REDIS_URL = f"redis://{_REDIS_HOST}:{_REDIS_PORT}"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": _REDIS_URL,
    }
}

CHANNEL_LAYERS["default"] = {
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    "CONFIG": {"hosts": [(_REDIS_HOST, _REDIS_PORT)]},
}

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_NAME = "__Secure-sessionid"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_NAME = "__Secure-csrftoken"

EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")

STATIC_ROOT = "/var/www/django/static"
MEDIA_ROOT = "/var/www/django/media"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
        )
    },
}

_SENTRY_DSN = env.str("SENTRY_DSN", None)
if _SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(
        dsn=_SENTRY_DSN,
        max_request_body_size="always",
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", 0.0),
    )
else:
    _ADMIN_EMAILS = env.str("ADMIN_EMAILS", None)
    if _ADMIN_EMAILS:
        from email.utils import getaddresses

        ADMINS = getaddresses([_ADMIN_EMAILS])
