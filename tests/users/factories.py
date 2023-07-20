from __future__ import annotations

from factory import Faker
from factory.django import DjangoModelFactory, Password

from socnet.users.models import User


class UserFactory(DjangoModelFactory):
    about = Faker("paragraph")
    birth_date = Faker("date_of_birth")
    display_name = Faker("name")
    email = Faker("email")
    location = Faker("address")
    password = Password("pw")
    username = Faker("user_name")

    class Meta:
        model = User
        django_get_or_create = ["email", "username"]
