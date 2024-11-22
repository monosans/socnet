from __future__ import annotations

from django.urls import path

from socnet.messenger import consumers

websocket_urlpatterns = [
    path("ws/chat/<int:interlocutor_pk>/", consumers.ChatConsumer.as_asgi())
]
