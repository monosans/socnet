from __future__ import annotations

from django.test import Client
from django.urls import reverse

from socnet.users.models import User

from ...users.factories import UserFactory
from ...utils import auth_client, parametrize_by_auth


def get_url(user: User) -> str:
    return reverse("blog:subscribers", args=(user.username,))


@parametrize_by_auth
def test_get(client: Client, *, auth: bool) -> None:
    if auth:
        auth_client(client)
    user = UserFactory()
    url = get_url(user)
    response = client.get(url)
    assert response.status_code == 200
    subscriber = UserFactory()
    subscriber.subscriptions.add(user)
    response = client.get(url)
    assert response.status_code == 200


def test_authed_get_self(client: Client) -> None:
    user = auth_client(client)
    url = get_url(user)
    response = client.get(url)
    assert response.status_code == 200
    subscriber = UserFactory()
    subscriber.subscriptions.add(user)
    response = client.get(url)
    assert response.status_code == 200
