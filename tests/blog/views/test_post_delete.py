from __future__ import annotations

from django.test import Client
from django.urls import reverse

from socnet.blog import models

from ...utils import auth_client, parametrize_by_auth
from .. import factories

factory = factories.PostFactory


def get_url(post: models.Post) -> str:
    return reverse("blog:post_delete", args=(post.pk,))


@parametrize_by_auth
def test_unauthed_get(client: Client, *, auth: bool) -> None:
    if auth:
        auth_client(client)
    post = factory()
    url = get_url(post)
    response = client.get(url)
    assert response.status_code == 405
    assert models.Post.objects.filter(pk=post.pk).exists()


def test_unauthed_post(client: Client) -> None:
    post = factory()
    url = get_url(post)
    response = client.post(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200
    assert models.Post.objects.filter(pk=post.pk).exists()


def test_non_author_post(client: Client) -> None:
    user = auth_client(client)
    post = factory()
    url = get_url(post)
    response = client.post(url, follow=True)
    assert response.redirect_chain == [
        (reverse("blog:user_posts", args=(user.get_username(),)), 302)
    ]
    assert response.status_code == 200
    assert models.Post.objects.filter(pk=post.pk).exists()


def test_author_post(client: Client) -> None:
    user = auth_client(client)
    post = factory(author=user)
    url = get_url(post)
    response = client.post(url, follow=True)
    assert response.redirect_chain == [
        (reverse("blog:user_posts", args=(user.get_username(),)), 302)
    ]
    assert response.status_code == 200
    assert not models.Post.objects.filter(pk=post.pk).exists()
