from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MainConfig(AppConfig):
    name = "server.apps.main"
    verbose_name = _("Main")

    def ready(self) -> None:
        from . import signals
