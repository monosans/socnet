import socket

from .base import *

DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += ["debug_toolbar", "extra_checks"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = [
    "{}.1".format(ip[: ip.rfind(".")])
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]
] + ["127.0.0.1", "10.0.2.2"]

MEDIA_ROOT = BASE_DIR / "media"

EXTRA_CHECKS = {
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
    ]
}
