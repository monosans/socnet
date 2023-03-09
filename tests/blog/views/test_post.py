from __future__ import annotations

from django.test import Client
from django.urls import reverse

from socnet.blog import models

from ...conftest import AuthedClient
from ...utils import assert_count_diff
from .. import factories


def get_url(post: models.Post) -> str:
    return reverse("blog:post", args=(post.pk,))


def test_unauthed_get(client: Client) -> None:
    post = factories.PostFactory()
    with assert_count_diff(models.Comment, 0):
        response = client.get(get_url(post))
    assert response.status_code == 200


def test_authed_get(authed_client: AuthedClient) -> None:
    test_unauthed_get(authed_client.client)


def test_unauthed_post(client: Client) -> None:
    post = factories.PostFactory()
    url = get_url(post)
    with assert_count_diff(models.Comment, 0):
        response = client.post(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200


def test_authed_post(authed_client: AuthedClient) -> None:
    client, user = authed_client
    post = factories.PostFactory()
    content = "comment content"
    with assert_count_diff(models.Comment, 1):
        response = client.post(get_url(post), data={"content": content})
    assert response.status_code == 200
    comment = models.Comment.objects.order_by("-pk").get()
    assert comment.author == user
    assert comment.content == content


def test_authed_post_empty(authed_client: AuthedClient) -> None:
    client = authed_client.client
    post = factories.PostFactory()
    with assert_count_diff(models.Comment, 0):
        response = client.post(get_url(post))
    assert response.status_code == 200
