from __future__ import annotations

from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker

from socnet.messenger import models
from tests.users.factories import UserFactory


class MessageFactory(DjangoModelFactory[models.Message]):
    sender = SubFactory(UserFactory)
    recipient = SubFactory(UserFactory)
    content = Faker("text")

    class Meta:
        model = models.Message
