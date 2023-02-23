from __future__ import annotations

from django.test import Client
from django.urls import reverse

from socnet.users.models import User

from ...conftest import AuthedClient
from ...users.factories import UserFactory


def get_url(user: User) -> str:
    return reverse("blog:subscriptions", args=(user.get_username(),))


def test_unauthed_get(client: Client) -> None:
    user = UserFactory()
    response = client.get(get_url(user))
    assert response.status_code == 200
    subscription = UserFactory()
    user.subscriptions.add(subscription)
    response = client.get(get_url(user))
    assert response.status_code == 200


def test_authed_get(authed_client: AuthedClient) -> None:
    test_unauthed_get(authed_client.client)


def test_authed_get_self(authed_client: AuthedClient) -> None:
    client, user = authed_client
    response = client.get(get_url(user))
    assert response.status_code == 200
    subscription = UserFactory()
    user.subscriptions.add(subscription)
    response = client.get(get_url(user))
    assert response.status_code == 200


def test_unauthed_post(client: Client) -> None:
    user = UserFactory()
    response = client.post(get_url(user))
    assert response.status_code == 405


def test_authed_post(authed_client: AuthedClient) -> None:
    client, user = authed_client
    response = client.post(get_url(user))
    assert response.status_code == 405
