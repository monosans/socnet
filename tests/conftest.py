from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pytest
from django.conf import LazySettings
from django.test import Client

from socnet.users.models import User

from .test_users.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_root(settings: LazySettings, tmp_path: Path) -> None:
    settings.MEDIA_ROOT = str(tmp_path.resolve())


@pytest.fixture()
def authed_client(client: Client) -> Client:
    user = UserFactory()
    client.force_login(user)
    return client


@pytest.fixture()
def authed_client_user(client: Client) -> Tuple[Client, User]:
    user = UserFactory()
    client.force_login(user)
    return client, user
