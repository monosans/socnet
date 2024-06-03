from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse

from ...users.factories import UserFactory
from ...utils import auth_client, parametrize_by_auth

if TYPE_CHECKING:
    from django.test import Client

    from socnet.users.models import User


def get_url(user: User) -> str:
    return reverse("blog:subscriptions", args=(user.username,))


@parametrize_by_auth
def test_get(client: Client, *, auth: bool) -> None:
    if auth:
        auth_client(client)
    user = UserFactory()
    url = get_url(user)
    response = client.get(url)
    assert response.status_code == 200
    subscription = UserFactory()
    user.subscriptions.add(subscription)
    response = client.get(url)
    assert response.status_code == 200


def test_authed_get_self(client: Client) -> None:
    user = auth_client(client)
    url = get_url(user)
    response = client.get(url)
    assert response.status_code == 200
    subscription = UserFactory()
    user.subscriptions.add(subscription)
    response = client.get(url)
    assert response.status_code == 200
