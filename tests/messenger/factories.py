from __future__ import annotations

from factory.django import DjangoModelFactory

from socnet.messenger import models


class ChatFactory(DjangoModelFactory):
    class Meta:
        model = models.Chat
