from __future__ import annotations

import socket

# pylint: disable-next=wildcard-import,unused-wildcard-import
from .base import *

DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += ["debug_toolbar", "extra_checks"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

TEMPLATES[0]["OPTIONS"][  # type: ignore[index]
    "string_if_invalid"
] = "INVALID EXPRESSION: %s"

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = [
    ip[: ip.rfind(".")] + ".1"
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]
] + ["127.0.0.1", "10.0.2.2"]

MEDIA_ROOT = str(APPS_DIR / "media")

EXTRA_CHECKS = {
    "checks": [
        "no-unique-together",
        "no-index-together",
        "model-admin",
        "field-file-upload-to",
        "field-verbose-name",
        "field-verbose-name-gettext",
        "field-verbose-name-gettext-case",
        "field-help-text-gettext",
        "field-text-null",
        "field-null",
        "field-foreign-key-db-index",
        "field-related-name",
        "field-default-null",
        "field-choices-constraint",
        "drf-model-serializer-extra-kwargs",
    ]
}
