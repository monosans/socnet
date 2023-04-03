from __future__ import annotations

from django.test import Client
from django.urls import reverse

from socnet.blog import models

from ...utils import assert_count_diff, auth_client, parametrize_by_auth
from .. import factories


def get_url(post: models.Post) -> str:
    return reverse("blog:post_delete", args=(post.pk,))


@parametrize_by_auth
def test_unauthed_get(client: Client, *, auth: bool) -> None:
    if auth:
        auth_client(client)
    post = factories.PostFactory()
    with assert_count_diff(models.Post, 0):
        response = client.get(get_url(post))
    assert response.status_code == 405


def test_unauthed_post(client: Client) -> None:
    post = factories.PostFactory()
    with assert_count_diff(models.Post, 0):
        response = client.post(get_url(post), follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), get_url(post)), 302)
    ]
    assert response.status_code == 200


def test_non_author_post(client: Client) -> None:
    user = auth_client(client)
    post = factories.PostFactory()
    with assert_count_diff(models.Post, 0):
        response = client.post(get_url(post), follow=True)
    assert response.redirect_chain == [
        (reverse("blog:user_posts", args=(user.get_username(),)), 302)
    ]
    assert response.status_code == 200


def test_author_post(client: Client) -> None:
    user = auth_client(client)
    post = factories.PostFactory(author=user)
    with assert_count_diff(models.Post, -1):
        response = client.post(get_url(post), follow=True)
    assert response.redirect_chain == [
        (reverse("blog:user_posts", args=(user.get_username(),)), 302)
    ]
    assert response.status_code == 200
