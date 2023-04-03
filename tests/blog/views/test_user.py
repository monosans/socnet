from __future__ import annotations

from django.test import Client
from django.urls import reverse

from socnet.users.models import User

from ...users.factories import UserFactory
from ...utils import auth_client, parametrize_by_auth_self


def get_url(user: User) -> str:
    return reverse("blog:user", args=(user.get_username(),))


@parametrize_by_auth_self
def test_get(client: Client, *, auth: bool, self: bool) -> None:
    if auth and self:
        user = auth_client(client)
    elif auth:
        auth_client(client)
        user = UserFactory()
    else:
        user = UserFactory()
    response = client.get(get_url(user))
    assert response.status_code == 200
