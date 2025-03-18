from __future__ import annotations

from config.settings.base import *

ALLOWED_HOSTS = [env.str("DOMAIN_NAME")]

MIDDLEWARE.remove("socnet.core.middleware.ResponseHeadersMiddleware")

_REDIS_URL = f"redis://{env.str('REDIS_HOST')}:{env.int('REDIS_PORT')}"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{_REDIS_URL}/{env.int('REDIS_CACHE_DB')}",
    }
}

CHANNEL_LAYERS["default"] = {
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    "CONFIG": {"hosts": [f"{_REDIS_URL}/{env.int('REDIS_CHANNELS_DB')}"]},
}

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_NAME = "__Secure-sessionid"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_NAME = "__Secure-csrftoken"

DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
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

if _SENTRY_DSN := env.str("SENTRY_DSN", None):
    import sentry_sdk
    from sentry_sdk.integrations.asyncio import AsyncioIntegration

    sentry_sdk.init(dsn=_SENTRY_DSN, integrations=(AsyncioIntegration(),))
elif _ADMIN_EMAILS := env.str("ADMIN_EMAILS", None):
    from email.utils import getaddresses

    ADMINS = getaddresses([_ADMIN_EMAILS])
