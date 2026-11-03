from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.blog.factories import CommentFactory, PostFactory
from tests.users.factories import UserFactory
from tests.utils import auth_client

if TYPE_CHECKING:
    from django.test import Client

parametrize_by_likeable = pytest.mark.parametrize(
    ("factory", "prefix"), [(PostFactory, "posts"), (CommentFactory, "comments")]
)


@parametrize_by_likeable
def test_like_unauthed(client: Client, factory: type[PostFactory], prefix: str) -> None:
    obj = factory.create()
    url = f"/api/{prefix}/{obj.pk}/likes"
    assert client.post(url).status_code == 401
    assert client.delete(url).status_code == 401
    assert not obj.likers.exists()


@parametrize_by_likeable
def test_like_and_unlike(client: Client, factory: type[PostFactory], prefix: str) -> None:
    user = auth_client(client)
    obj = factory.create()
    other_liker = UserFactory.create()
    obj.likers.add(other_liker)
    url = f"/api/{prefix}/{obj.pk}/likes"

    response = client.post(url)
    assert response.status_code == 201
    assert set(obj.likers.all()) == {user, other_liker}

    # Liking twice is idempotent.
    assert client.post(url).status_code == 201
    assert obj.likers.count() == 2

    response = client.delete(url)
    assert response.status_code == 204
    assert list(obj.likers.all()) == [other_liker]

    # Removing a like that is not there is idempotent too.
    assert client.delete(url).status_code == 204
    assert list(obj.likers.all()) == [other_liker]


@parametrize_by_likeable
def test_like_missing(client: Client, factory: type[PostFactory], prefix: str) -> None:
    auth_client(client)
    obj = factory.create()
    url = f"/api/{prefix}/{obj.pk + 1}/likes"
    assert client.post(url).status_code == 404
    assert client.delete(url).status_code == 404


@pytest.mark.parametrize("prefix", ["posts", "comments"])
def test_like_non_positive_id(client: Client, prefix: str) -> None:
    auth_client(client)
    assert client.post(f"/api/{prefix}/0/likes").status_code == 422


def test_subscription_unauthed(client: Client) -> None:
    to_user = UserFactory.create()
    url = f"/api/users/{to_user.username}/subscriptions"
    assert client.post(url).status_code == 401
    assert client.delete(url).status_code == 401
    assert not to_user.subscribers.exists()


def test_subscribe_and_unsubscribe(client: Client) -> None:
    user = auth_client(client)
    to_user = UserFactory.create()
    url = f"/api/users/{to_user.username}/subscriptions"

    response = client.post(url)
    assert response.status_code == 201
    assert list(user.subscriptions.all()) == [to_user]
    assert not to_user.subscriptions.exists()

    response = client.delete(url)
    assert response.status_code == 204
    assert not user.subscriptions.exists()


def test_subscribe_username_case_insensitive(client: Client) -> None:
    user = auth_client(client)
    to_user = UserFactory.create(username="Someone")
    response = client.post("/api/users/sOMEONE/subscriptions")
    assert response.status_code == 201
    assert list(user.subscriptions.all()) == [to_user]


def test_subscription_missing_user(client: Client) -> None:
    user = auth_client(client)
    url = "/api/users/nobody/subscriptions"
    assert client.post(url).status_code == 404
    assert client.delete(url).status_code == 404
    assert not user.subscriptions.exists()


def test_subscribe_to_self(client: Client) -> None:
    user = auth_client(client)
    response = client.post(f"/api/users/{user.username}/subscriptions")
    assert response.status_code == 400
    assert response.json() == {"detail": "You can't subscribe to yourself."}
    assert not user.subscriptions.exists()
