from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from typing_extensions import override


class UsersConfig(AppConfig):
    name = "socnet.users"
    verbose_name = _("Users")

    @override
    def ready(self) -> None:
        from . import signals  # noqa: F401
