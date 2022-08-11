from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "socnet.users"
    verbose_name = _("Users")

    def ready(self) -> None:
        # pylint: disable-next=import-outside-toplevel,unused-import
        from . import signals
