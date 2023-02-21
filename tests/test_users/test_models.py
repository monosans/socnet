from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from socnet.users.models import User

from . import factories

pytestmark = pytest.mark.django_db


class TestUser:
    factory = factories.UserFactory

    def test_username_uppercase_forbidden(self) -> None:
        user = self.factory.build(username="USER")
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_username_lowercase_allowed(self) -> None:
        user = self.factory.build(username="user")
        user.full_clean()
        assert user.get_username() == "user"

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
