from __future__ import annotations

from django.test import Client
from django.urls import reverse, reverse_lazy

from socnet.blog import models

from ...utils import (
    ClientMethods,
    assert_count_diff,
    auth_client,
    parametrize_by_get_post,
)

url = reverse_lazy("blog:post_create")


@parametrize_by_get_post
def test_unauthed(client: Client, method: ClientMethods) -> None:
    with assert_count_diff(models.Post, 0):
        response = (
            client.get(url, follow=True)
            if method == ClientMethods.GET
            else client.post(url, follow=True)
        )
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200


@parametrize_by_get_post
def test_authed(client: Client, method: ClientMethods) -> None:
    auth_client(client)
    with assert_count_diff(models.Post, 0):
        response = client.get(url) if method == ClientMethods.GET else client.post(url)
    assert response.status_code == 200


def test_authed_post(client: Client) -> None:
    user = auth_client(client)
    content = " post content "
    with assert_count_diff(models.Post, 1):
        response = client.post(url, data={"content": content}, follow=True)
    assert response.status_code == 200
    post = models.Post.objects.order_by("-pk").get()
    assert post.author == user
    assert post.content == content.strip()
    assert response.redirect_chain == [(post.get_absolute_url(), 302)]
