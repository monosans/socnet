from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MainConfig(AppConfig):
    name = "socnet.main"
    verbose_name = _("Main")

    def ready(self) -> None:
        # pylint: disable-next=import-outside-toplevel,unused-import
        from . import signals
