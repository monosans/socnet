from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse_lazy

from tests.blog.factories import PostFactory
from tests.users.factories import UserFactory
from tests.utils import auth_client, parametrize_by_auth

if TYPE_CHECKING:
    from django.test import Client

url = reverse_lazy("blog:posts")


def test_unauthed_get(client: Client) -> None:
    response = client.get(url)
    assert response.status_code == 200


@parametrize_by_auth
def test_get_empty_search(client: Client, *, auth: bool) -> None:
    if auth:
        auth_client(client)
    response = client.get(f"{url}?q=")
    assert response.status_code == 200


def test_feed_shows_subscriptions_posts(client: Client) -> None:
    user = auth_client(client)
    followed = UserFactory.create()
    user.subscriptions.add(followed)
    older, newer = PostFactory.create_batch(2, author=followed)
    PostFactory.create()
    PostFactory.create(author=user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.templates[0].name == "blog/posts.html"
    assert list(response.context["posts"]) == [newer, older]
    assert not response.context["is_search"]


def test_feed_without_subscriptions(client: Client) -> None:
    auth_client(client)
    PostFactory.create()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["posts"] is None
    assert "Subscribe to users you are interested in" in response.content.decode()


def test_feed_htmx_pagination(client: Client) -> None:
    user = auth_client(client)
    followed = UserFactory.create()
    user.subscriptions.add(followed)
    posts = PostFactory.create_batch(11, author=followed)
    response = client.get(url, data={"page": 2}, headers={"hx-request": "true"})
    assert response.status_code == 200
    assert response.templates[0].name == "blog/inc/posts_preview.html"
    assert list(response.context["posts"]) == [posts[0]]
    assert "HX-Request" in response["Vary"]
    response = client.get(url, headers={"hx-request": "true"})
    assert 'hx-get="?page=2"' in response.content.decode()


@parametrize_by_auth
def test_search_finds_posts(client: Client, *, auth: bool) -> None:
    if auth:
        auth_client(client)
    found = PostFactory.create(content="An essay about pineapples")
    PostFactory.create(content="Something else entirely")
    response = client.get(url, data={"q": "pineapples"})
    assert response.status_code == 200
    assert list(response.context["posts"]) == [found]
    assert response.context["is_search"]


def test_search_no_results(client: Client) -> None:
    PostFactory.create(content="Something else entirely")
    response = client.get(url, data={"q": "pineapples"})
    assert response.status_code == 200
    assert response.context["posts"] is None
    assert "No posts found." in response.content.decode()


def test_search_whitespace_query(client: Client) -> None:
    response = client.get(url, data={"q": " "})
    assert response.status_code == 200
    assert response.context["posts"] is None
    assert response.context["form"].errors == {"q": ["This field is required."]}
    assert "No posts found." not in response.content.decode()
