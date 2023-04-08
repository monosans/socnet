from __future__ import annotations

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from socnet.messenger import models

from ..users.factories import UserFactory


class MessageFactory(DjangoModelFactory):
    sender = SubFactory(UserFactory)
    recipient = SubFactory(UserFactory)
    content = Faker("text")

    class Meta:
        model = models.Message
