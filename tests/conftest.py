from __future__ import annotations

from pathlib import Path
from typing import List, NamedTuple

import pytest
from django.conf import LazySettings
from django.test import Client

from socnet.users.models import User

from .users.factories import UserFactory


def pytest_collection_modifyitems(items: List[pytest.Item]) -> None:
    for item in items:
        item.add_marker("django_db")


@pytest.fixture(autouse=True)
def _media_root(settings: LazySettings, tmp_path: Path) -> None:
    settings.MEDIA_ROOT = str(tmp_path.resolve())


class AuthedClient(NamedTuple):
    client: Client
    user: User


@pytest.fixture
def authed_client(client: Client) -> AuthedClient:
    user = UserFactory()
    client.force_login(user)
    return AuthedClient(client, user)
