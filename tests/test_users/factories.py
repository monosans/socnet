from __future__ import annotations

from typing import Type

from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory

from socnet.users.models import User as UserType


class UserFactory(DjangoModelFactory):  # type: ignore[misc]
    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    birth_date = Faker("date_of_birth")
    location = Faker("address")
    about = Faker("paragraph")
    password = Faker("password")

    class Meta:
        model: Type[UserType] = get_user_model()
        django_get_or_create = ["username"]
