from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "socnet.users"
    verbose_name = _("Users")

    def ready(
        self,  # noqa: PLR6301
    ) -> None:
        from . import signals  # noqa: F401
