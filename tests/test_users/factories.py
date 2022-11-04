from __future__ import annotations

from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):  # type: ignore[misc]
    about = Faker("paragraph")
    birth_date = Faker("date_of_birth")
    display_name = Faker("name")
    email = Faker("email")
    location = Faker("address")
    password = Faker("password")
    username = Faker("user_name")

    class Meta:
        model = get_user_model()
        django_get_or_create = ["email", "username"]
