from __future__ import annotations

import logging
from typing import override

from django.conf import settings


class RequireAdmins(logging.Filter):
    @override
    def filter(self, record: logging.LogRecord) -> bool:
        return settings.configured and bool(settings.ADMINS)
