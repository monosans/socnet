from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MessengerConfig(AppConfig):
    name = "socnet.messenger"
    verbose_name = _("Messenger")
