from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from socnet.blog import models
from tests.blog import factories
from tests.utils import auth_client, parametrize_by_auth

if TYPE_CHECKING:
    from django.test import Client

factory = factories.PostFactory


def get_url(post: models.Post) -> str:
    return reverse("blog:post_delete", args=(post.pk,))


@parametrize_by_auth
def test_unauthed_get(client: Client, *, auth: bool) -> None:
    if auth:
        auth_client(client)
    post = factory.create()
    url = get_url(post)
    response = client.get(url)
    assert response.status_code == 405
    assert models.Post.objects.filter(pk=post.pk).exists()


def test_unauthed_post(client: Client) -> None:
    post = factory.create()
    url = get_url(post)
    response = client.post(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200
    assert models.Post.objects.filter(pk=post.pk).exists()


@pytest.mark.parametrize("is_author", [True, False])
def test_authed_post(client: Client, *, is_author: bool) -> None:
    user = auth_client(client)
    post = factory.create(author=user) if is_author else factory.create()
    url = get_url(post)
    response = client.post(url, follow=True)
    assert response.redirect_chain == [
        (reverse("blog:user_posts", args=(user.username,)), 302)
    ]
    assert response.status_code == 200
    assert is_author != models.Post.objects.filter(pk=post.pk).exists()
