from django.apps import AppConfig


class MessengerConfig(AppConfig):
    name = "server.apps.messenger"

    def ready(self) -> None:
        from . import signals
