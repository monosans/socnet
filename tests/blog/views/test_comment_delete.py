from __future__ import annotations

import pytest
from django.test import Client
from django.urls import reverse

from socnet.blog import models

from ...utils import auth_client, parametrize_by_auth
from .. import factories

factory = factories.CommentFactory


def get_url(comment: models.Comment) -> str:
    return reverse("blog:comment_delete", args=(comment.pk,))


@parametrize_by_auth
def test_get(client: Client, *, auth: bool) -> None:
    if auth:
        auth_client(client)
    comment = factory()
    url = get_url(comment)
    response = client.get(url)
    assert response.status_code == 405
    assert models.Comment.objects.filter(pk=comment.pk).exists()


def test_unauthed_post(client: Client) -> None:
    comment = factory()
    url = get_url(comment)
    response = client.post(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200
    assert models.Comment.objects.filter(pk=comment.pk).exists()


@pytest.mark.parametrize("is_author", [True, False])
def test_authed_post(client: Client, *, is_author: bool) -> None:
    user = auth_client(client)
    comment = factory(author=user) if is_author else factory()
    url = get_url(comment)
    response = client.post(url, follow=True)
    assert response.redirect_chain == [(user.get_absolute_url(), 302)]
    assert response.status_code == 200
    assert is_author != models.Comment.objects.filter(pk=comment.pk).exists()


def test_author_post_with_redirect(client: Client) -> None:
    user = auth_client(client)
    comment = factory(author=user)
    url = get_url(comment)
    next_url = comment.post.get_absolute_url()
    response = client.post(f"{url}?next={next_url}", follow=True)
    assert response.redirect_chain == [(next_url, 302)]
    assert response.status_code == 200
    assert not models.Comment.objects.filter(pk=comment.pk).exists()


def test_post_author_post(client: Client) -> None:
    user = auth_client(client)
    post = factories.PostFactory(author=user)
    comment = factory(post=post)
    url = get_url(comment)
    response = client.post(url, follow=True)
    assert response.redirect_chain == [(user.get_absolute_url(), 302)]
    assert response.status_code == 200
    assert not models.Comment.objects.filter(pk=comment.pk).exists()
