from __future__ import annotations

from typing import Optional

from .base import *

ALLOWED_HOSTS = [env.str("DOMAIN_NAME")]

DATABASES["default"]["CONN_MAX_AGE"] = 60

_REDIS_HOST = "redis"
_REDIS_PORT = 6379
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
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000

EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")

STATIC_ROOT = "/var/www/django/static"
MEDIA_ROOT = "/var/www/django/media"

LOGGING["loggers"]["gunicorn"] = {}  # type: ignore[index]
_SENTRY_DSN: Optional[str] = env.str("SENTRY_DSN", None)
if _SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.redis import RedisIntegration

    sentry_sdk.init(
        dsn=_SENTRY_DSN,
        integrations=(DjangoIntegration(), RedisIntegration()),
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", 0.0),
    )
    LOGGING["loggers"]["sentry_sdk"] = {}  # type: ignore[index]
else:
    _ADMIN_EMAILS: Optional[str] = env.str("ADMIN_EMAILS", None)
    if _ADMIN_EMAILS:
        from email.utils import getaddresses

        ADMINS = getaddresses([_ADMIN_EMAILS])
        LOGGING["handlers"]["mail_admins"] = {  # type: ignore[index]
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        }
        LOGGING["root"]["handlers"].append("mail_admins")  # type: ignore[index]
