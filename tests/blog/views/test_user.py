from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse

from ...users.factories import UserFactory
from ...utils import auth_client, parametrize_by_auth_self

if TYPE_CHECKING:
    from django.test import Client

    from socnet.users.models import User


def get_url(user: User) -> str:
    return reverse("blog:user", args=(user.username,))


@parametrize_by_auth_self
def test_get(client: Client, *, auth: bool, self: bool) -> None:
    if auth and self:
        user = auth_client(client)
    elif auth:
        auth_client(client)
        user = UserFactory()
    else:
        user = UserFactory()
    url = get_url(user)
    response = client.get(url)
    assert response.status_code == 200
