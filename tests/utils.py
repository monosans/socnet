from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

import pytest

from tests.users.factories import UserFactory

if TYPE_CHECKING:
    from typing import Any

    from django.test import Client

    from socnet.users.models import User


def auth_client(client: Client, **kwargs: Any) -> User:
    user = UserFactory.create(**kwargs)
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
