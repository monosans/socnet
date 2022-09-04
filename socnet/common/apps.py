from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommonConfig(AppConfig):
    name = "socnet.common"
    verbose_name = _("Common")

    def ready(self) -> None:
        # pylint: disable-next=import-outside-toplevel,unused-import
        from . import signals
