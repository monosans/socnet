from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MessengerConfig(AppConfig):
    name = "server.apps.messenger"
    verbose_name = _("Messenger")

    def ready(self) -> None:
        from . import signals
