from __future__ import annotations

import re
from datetime import UTC, date, datetime, timedelta

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone

from socnet.users.exceptions import SelfSubscriptionError
from socnet.users.models import User
from tests.users import factories

factory = factories.UserFactory


@pytest.mark.parametrize(
    ("username", "exc_str"),
    [
        (
            "пользователь",
            re.escape(
                "{'username': ['Enter a valid “slug” consisting of letters,"
                " numbers, underscores or hyphens.']}"
            ),
        ),
        (
            "user!",
            re.escape(
                "{'username': ['Enter a valid “slug” consisting of letters,"
                " numbers, underscores or hyphens.']}"
            ),
        ),
        ("", re.escape("{'username': ['This field cannot be blank.']}")),
    ],
)
def test_username_forbidden_patterns(username: str, exc_str: str) -> None:
    user = factory.build(username=username)
    with pytest.raises(ValidationError, match=exc_str):
        user.full_clean()


@pytest.mark.parametrize("username", ["user", "user_1", "user-_", "a", "-", "_", "1"])
def test_username_allowed_patterns(username: str) -> None:
    user = factory.build(username=username)
    user.full_clean()
    assert user.username == username


def test_username_unique() -> None:
    factory.create(username="user")
    user2 = factory.build(username="user")
    exc_str = re.escape("{'username': ['A user with that username already exists.']}")
    with pytest.raises(ValidationError, match=exc_str):
        user2.full_clean()
    exc_str = re.escape(
        "duplicate key value violates unique constraint "
        '"users_user_username_06e46fe6_uniq"'
        "\nDETAIL:  Key (username)=(user) already exists."
    )
    with pytest.raises(IntegrityError, match=exc_str):
        user2.save()


def test_username_case_insensitive() -> None:
    factory.create(username="user")
    assert User.objects.filter(username="USER").exists()


def test_birth_date_unrealistically_old() -> None:
    user = factory.build(birth_date="1900-01-01")
    exc_str = re.escape("{'birth_date': ['Birth date is implausible.']}")
    with pytest.raises(ValidationError, match=exc_str):
        user.full_clean()


def test_birth_date_in_future() -> None:
    tomorrow = timezone.now() + timedelta(days=1)
    user = factory.build(birth_date=tomorrow)
    exc_str = re.escape("{'birth_date': ['Birth date cannot be in the future.']}")
    with pytest.raises(ValidationError, match=exc_str):
        user.full_clean()


def test_birth_date_today() -> None:
    tomorrow = timezone.now()
    user = factory.build(birth_date=tomorrow)
    user.full_clean()


def test_names_are_display_name() -> None:
    user = factory.build(display_name="Display Name")
    assert user.get_full_name() == "Display Name"
    assert user.get_short_name() == "Display Name"


def test_get_age_without_birth_date() -> None:
    assert factory.build(birth_date=None).get_age() is None


def test_get_age(monkeypatch: pytest.MonkeyPatch) -> None:
    now = datetime(2024, 6, 15, tzinfo=UTC)
    monkeypatch.setattr(timezone, "now", lambda: now)
    assert factory.build(birth_date=date(2000, 6, 15)).get_age() == 24
    assert factory.build(birth_date=date(2000, 6, 16)).get_age() == 23
    assert factory.build(birth_date=date(2000, 1, 1)).get_age() == 24
    assert factory.build(birth_date=date(2000, 12, 31)).get_age() == 23


def test_self_subscription_forbidden() -> None:
    user = factory.create()
    with (
        pytest.raises(SelfSubscriptionError, match=r"^You can't subscribe to yourself\.$"),
        transaction.atomic(),
    ):
        user.subscriptions.add(user)
    assert not user.subscriptions.exists()


def test_subscription_is_not_symmetrical() -> None:
    user, other = factory.create_batch(2)
    user.subscriptions.add(other)
    assert list(user.subscriptions.all()) == [other]
    assert list(other.subscribers.all()) == [user]
    assert not other.subscriptions.exists()
