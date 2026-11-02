from __future__ import annotations

import logging
from typing import override

from django.conf import settings
from django.utils import log


class RequireAdmins(logging.Filter):
    @override
    def filter(self, record: logging.LogRecord) -> bool:
        return settings.configured and bool(settings.ADMINS)


class AdminEmailHandler(log.AdminEmailHandler):
    """Mails the admins, without letting a failed send escape the log call.

    Once MAILERS is configured, Django's handler no longer sends with
    fail_silently, so an SMTP error would raise out of logger.error().
    """

    @override
    def emit(self, record: logging.LogRecord) -> None:
        try:
            super().emit(record)
        except Exception:
            self.handleError(record)
