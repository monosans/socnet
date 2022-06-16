import socket

from .common import DATABASES, INSTALLED_APPS, MIDDLEWARE
from .config import BASE_DIR

DEBUG = True

INSTALLED_APPS += ("debug_toolbar", "extra_checks")

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configure-internal-ips
INTERNAL_IPS = [
    "{}.1".format(ip[: ip.rfind(".")])
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]
] + ["127.0.0.1", "10.0.2.2"]

MEDIA_ROOT = BASE_DIR / "media"

EXTRA_CHECKS = {
    "include_apps": [
        "server.apps.api",
        "server.apps.messenger",
        "server.apps.users",
        "server.apps.main",
    ],
    "checks": [
        "drf-model-serializer-extra-kwargs",
        "field-boolean-null",
        "field-choices-constraint",
        "field-default-null",
        "field-file-upload-to",
        "field-foreign-key-db-index",
        "field-help-text-gettext",
        "field-null",
        "field-text-null",
        "field-verbose-name-gettext-case",
        "field-verbose-name-gettext",
        "field-verbose-name",
        "model-admin",
        "no-index-together",
        "no-unique-together",
    ],
}

# https://docs.djangoproject.com/en/4.0/ref/databases/#caveats
DATABASES["default"]["CONN_MAX_AGE"] = 0
