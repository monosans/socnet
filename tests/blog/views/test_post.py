from __future__ import annotations

import pytest
from django.test import Client
from django.urls import reverse

from socnet.blog import models

from ...utils import ClientMethods, assert_count_diff, auth_client
from .. import factories


def get_url(post: models.Post) -> str:
    return reverse("blog:post", args=(post.pk,))


@pytest.mark.parametrize(
    ("auth", "method"),
    [(False, ClientMethods.GET), (True, ClientMethods.GET), (True, ClientMethods.POST)],
)
def test_empty_request(client: Client, *, auth: bool, method: ClientMethods) -> None:
    if auth:
        auth_client(client)
    post = factories.PostFactory()
    url = get_url(post)
    with assert_count_diff(models.Comment, 0):
        response = client.get(url) if method == ClientMethods.GET else client.post(url)
    assert response.status_code == 200


def test_unauthed_post(client: Client) -> None:
    post = factories.PostFactory()
    url = get_url(post)
    with assert_count_diff(models.Comment, 0):
        response = client.post(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200


def test_authed_post(client: Client) -> None:
    user = auth_client(client)
    post = factories.PostFactory()
    content = " comment content "
    with assert_count_diff(models.Comment, 1):
        response = client.post(get_url(post), data={"content": content})
    assert response.status_code == 200
    comment = models.Comment.objects.order_by("-pk").get()
    assert comment.author == user
    assert comment.content == content.strip()
