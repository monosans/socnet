from __future__ import annotations

from typing import override

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "socnet.users"
    verbose_name = _("Users")

    @override
    def ready(self) -> None:
        from socnet.users import signals  # noqa: F401, PLC0415
