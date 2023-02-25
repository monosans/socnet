from __future__ import annotations

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": (
                "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            )
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}
