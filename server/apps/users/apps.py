from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "server.apps.users"
    verbose_name = _("Users")
