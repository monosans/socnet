from __future__ import annotations

import logging

from django.conf import settings


class RequireAdmins(logging.Filter):
    def filter(
        self,  # noqa: PLR6301
        record: logging.LogRecord,  # noqa: ARG002
    ) -> bool:
        return settings.configured and bool(settings.ADMINS)
