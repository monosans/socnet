from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommonConfig(AppConfig):
    name = "socnet.common"
    verbose_name = _("Common")
