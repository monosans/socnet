from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
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

    @post_generation  # type: ignore[misc]
    def password(
        obj: UserType, create: bool, extracted: Any, **kwargs: Any
    ) -> None:
        if not isinstance(extracted, str):
            extracted = Faker("password").evaluate(
                None, None, extra={"locale": None}
            )
        obj.set_password(extracted)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
