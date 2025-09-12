from __future__ import annotations

from typing import TYPE_CHECKING

from factory.django import DjangoModelFactory, Password
from factory.faker import Faker

from socnet.users.models import User

if TYPE_CHECKING:
    from typing import ClassVar


class UserFactory(DjangoModelFactory[User]):
    about = Faker("paragraph")
    birth_date = Faker("date_of_birth")
    display_name = Faker("name")
    email = Faker("email")
    location = Faker("address")
    password = Password("pw")
    username = Faker("user_name")

    class Meta:
        model = User
        django_get_or_create: ClassVar = ["email", "username"]
