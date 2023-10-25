from __future__ import annotations

import logging

from django.conf import settings
from typing_extensions import override


class RequireAdmins(logging.Filter):
    @override
    def filter(self, record: logging.LogRecord) -> bool:
        return settings.configured and bool(settings.ADMINS)
