from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogConfig(AppConfig):
    name = "socnet.blog"
    verbose_name = _("Blog")
