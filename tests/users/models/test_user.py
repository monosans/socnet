from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from socnet.users.models import User

from .. import factories

factory = factories.UserFactory


@pytest.mark.parametrize("username", ("пользователь", "user!", ""))
def test_username_forbidden_patterns(username: str) -> None:
    user = factory.build(username=username)
    with pytest.raises(ValidationError):
        user.full_clean()


@pytest.mark.parametrize(
    "username", ("user", "user_1", "user-_", "a", "-", "_", "1")
)
def test_username_allowed_patterns(username: str) -> None:
    user = factory.build(username=username)
    user.full_clean()
    assert user.get_username() == username


def test_username_unique() -> None:
    factory(username="user")
    user2 = factory.build(username="user")
    with pytest.raises(ValidationError):
        user2.full_clean()
    with pytest.raises(IntegrityError):
        user2.save()


def test_username_case_insensitive() -> None:
    factory(username="user")
    assert User.objects.filter(username="USER").exists()
