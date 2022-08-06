from __future__ import annotations

from pathlib import Path

import pytest
from django.conf import LazySettings
from django.test import Client

from socnet.users.models import User as UserType

from .test_users.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_root(settings: LazySettings, tmp_path: Path) -> None:
    settings.MEDIA_ROOT = str(tmp_path.resolve())


@pytest.fixture()
def user(
    # pylint: disable-next=unused-argument
    db: None,
) -> UserType:
    return UserFactory()


@pytest.fixture()
def authed_client(
    client: Client,
    # pylint: disable-next=redefined-outer-name
    user: UserType,
) -> Client:
    client.force_login(user)
    return client
