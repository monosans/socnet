from django.apps import AppConfig


class MainConfig(AppConfig):
    name = "server.apps.main"

    def ready(self) -> None:
        from . import signals
