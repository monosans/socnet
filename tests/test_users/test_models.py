from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from socnet.users.models import User

from . import factories

pytestmark = pytest.mark.django_db


class TestUser:
    factory = factories.UserFactory

    @pytest.mark.parametrize(
        "username", ("User", "1user", "_user", "user_", "1", "_", "")
    )
    def test_username_forbidden_patterns(self, username: str) -> None:
        user = self.factory.build(username=username)
        with pytest.raises(ValidationError):
            user.full_clean()

    @pytest.mark.parametrize("username", ("user", "user1", "user_user", "a"))
    def test_username_allowed_patterns(self, username: str) -> None:
        user = self.factory.build(username=username)
        user.full_clean()
        assert user.get_username() == username

    def test_username_unique(self) -> None:
        self.factory(username="user")
        user2 = self.factory.build(username="user")
        with pytest.raises(ValidationError):
            user2.full_clean()
        with pytest.raises(IntegrityError):
            user2.save()

    def test_username_case_insensitive(self) -> None:
        self.factory(username="user")
        assert User.objects.filter(username="USER").exists()
