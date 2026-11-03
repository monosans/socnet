from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse

from tests.users.factories import UserFactory
from tests.utils import auth_client, parametrize_by_auth, set_image

if TYPE_CHECKING:
    from django.test import Client

    from socnet.users.models import User


def get_url(user: User) -> str:
    return reverse("blog:subscribers", args=(user.username,))


@parametrize_by_auth
def test_get(client: Client, *, auth: bool) -> None:
    if auth:
        auth_client(client)
    user = UserFactory.create()
    url = get_url(user)
    response = client.get(url)
    assert response.status_code == 200
    subscriber = UserFactory.create()
    subscriber.subscriptions.add(user)
    response = client.get(url)
    assert response.status_code == 200


def test_authed_get_self(client: Client) -> None:
    user = auth_client(client)
    url = get_url(user)
    response = client.get(url)
    assert response.status_code == 200
    subscriber = UserFactory.create()
    subscriber.subscriptions.add(user)
    response = client.get(url)
    assert response.status_code == 200


def test_subscriber_image(client: Client) -> None:
    user = UserFactory.create()
    subscriber = UserFactory.create()
    subscriber.subscriptions.add(user)
    image_src = set_image(subscriber)
    response = client.get(get_url(user))
    assert response.status_code == 200
    assert list(response.context["subscribers"]) == [subscriber]
    assert image_src in response.content.decode()
