from __future__ import annotations

from factory.declarations import Sequence
from factory.django import DjangoModelFactory, Password
from factory.faker import Faker

from socnet.users.models import User


class UserFactory(DjangoModelFactory[User]):
    about = Faker("paragraph")
    birth_date = Faker("date_of_birth")
    display_name = Faker("name")
    email = Sequence(lambda n: f"user_{n}@example.com")
    location = Faker("address")
    password = Password("pw")
    username = Sequence(lambda n: f"user_{n}")

    class Meta:
        model = User
