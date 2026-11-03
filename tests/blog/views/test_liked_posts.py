from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse

from tests.blog import factories
from tests.users.factories import UserFactory
from tests.utils import auth_client, parametrize_by_auth_self

if TYPE_CHECKING:
    from django.test import Client

    from socnet.users.models import User


def get_url(user: User) -> str:
    return reverse("blog:liked_posts", args=(user.username,))


@parametrize_by_auth_self
def test_get(client: Client, *, auth: bool, self: bool) -> None:
    if auth and self:
        user = auth_client(client)
    elif auth:
        auth_client(client)
        user = UserFactory.create()
    else:
        user = UserFactory.create()
    url = get_url(user)
    response = client.get(url)
    assert response.status_code == 200
    post = factories.PostFactory.create(author=user)
    post.likers.add(user)
    response = client.get(url)
    assert response.status_code == 200


def test_only_liked_posts(client: Client) -> None:
    user = UserFactory.create()
    liked = factories.PostFactory.create_batch(11)
    for post in liked:
        post.likers.add(user)
    factories.PostFactory.create(author=user)
    url = get_url(user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["user"] == user
    assert list(response.context["posts"]) == liked[:0:-1]
    response = client.get(url, data={"page": 2}, headers={"hx-request": "true"})
    assert response.status_code == 200
    assert response.templates[0].name == "blog/inc/posts_preview.html"
    assert list(response.context["posts"]) == [liked[0]]


def test_missing_user(client: Client) -> None:
    assert client.get(reverse("blog:liked_posts", args=("nobody",))).status_code == 404
