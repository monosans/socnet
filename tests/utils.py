from __future__ import annotations

from contextlib import contextmanager
from enum import Enum, auto
from typing import Generator, Type

import pytest
from django.db.models import Model
from django.test import Client

from socnet.users.models import User

from .users.factories import UserFactory


@contextmanager
def assert_count_diff(model: Type[Model], diff: int) -> Generator[None, None, None]:
    enter_count = model.objects.count()
    yield
    assert model.objects.count() == enter_count + diff


def auth_client(client: Client) -> User:
    user = UserFactory()
    client.force_login(user)
    return user


class ClientMethods(Enum):
    GET = auto()
    POST = auto()


parametrize_by_get_post = pytest.mark.parametrize("method", ClientMethods)
parametrize_by_auth = pytest.mark.parametrize("auth", [True, False])
parametrize_by_auth_self = pytest.mark.parametrize(
    ("auth", "self"), [(True, True), (True, False), (False, False)]
)
