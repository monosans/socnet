from __future__ import annotations

import logging

from django.conf import settings


class RequireAdmins(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003, ARG002
        return settings.configured and bool(settings.ADMINS)
