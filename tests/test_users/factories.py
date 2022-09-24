from __future__ import annotations

from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory


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
        model = get_user_model()
        django_get_or_create = ["username"]
