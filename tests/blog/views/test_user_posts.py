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
    return reverse("blog:user_posts", args=(user.username,))


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


def test_htmx_pagination(client: Client) -> None:
    user = UserFactory.create()
    posts = factories.PostFactory.create_batch(11, author=user)
    factories.PostFactory.create()
    url = get_url(user)
    response = client.get(url)
    assert response.status_code == 200
    assert list(response.context["posts"]) == posts[:0:-1]
    assert 'hx-get="?page=2"' in response.content.decode()
    response = client.get(url, data={"page": 2}, headers={"hx-request": "true"})
    assert response.status_code == 200
    assert response.templates[0].name == "blog/inc/posts_preview.html"
    assert list(response.context["posts"]) == [posts[0]]


def test_is_liked(client: Client) -> None:
    viewer = auth_client(client)
    user = UserFactory.create()
    not_liked, liked = factories.PostFactory.create_batch(2, author=user)
    liked.likers.add(viewer)
    response = client.get(get_url(user))
    assert response.status_code == 200
    assert [(p, p.is_liked) for p in response.context["posts"]] == [
        (liked, True),
        (not_liked, False),
    ]


def test_missing_user(client: Client) -> None:
    assert client.get(reverse("blog:user_posts", args=("nobody",))).status_code == 404
