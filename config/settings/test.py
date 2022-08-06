from __future__ import annotations

# pylint: disable-next=wildcard-import,unused-wildcard-import
from .base import *

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
for template in TEMPLATES:
    template["OPTIONS"]["debug"] = True  # type: ignore[index]
