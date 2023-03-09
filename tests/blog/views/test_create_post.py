from __future__ import annotations

from django.test import Client
from django.urls import reverse, reverse_lazy

from socnet.blog import models

from ...conftest import AuthedClient
from ...utils import assert_count_diff

url = reverse_lazy("blog:post_create")


def test_unauthed_get(client: Client) -> None:
    with assert_count_diff(models.Post, 0):
        response = client.get(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200


def test_unauthed_post(client: Client) -> None:
    with assert_count_diff(models.Post, 0):
        response = client.post(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200


def test_authed_get(authed_client: AuthedClient) -> None:
    client = authed_client.client
    with assert_count_diff(models.Post, 0):
        response = client.get(url)
    assert response.status_code == 200


def test_authed_post_empty(authed_client: AuthedClient) -> None:
    client = authed_client.client
    with assert_count_diff(models.Post, 0):
        response = client.post(url)
    assert response.status_code == 200


def test_authed_post(authed_client: AuthedClient) -> None:
    client, user = authed_client
    content = "post_content"
    with assert_count_diff(models.Post, 1):
        response = client.post(url, data={"content": content}, follow=True)
    assert response.status_code == 200
    post = models.Post.objects.order_by("-pk").get()
    assert post.author == user
    assert post.content == content
    assert response.redirect_chain == [(post.get_absolute_url(), 302)]
