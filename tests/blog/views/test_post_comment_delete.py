from __future__ import annotations

from django.test import Client
from django.urls import reverse

from socnet.blog import models

from ...utils import assert_count_diff, auth_client, parametrize_by_auth
from .. import factories


def get_url(comment: models.Comment) -> str:
    return reverse("blog:comment_delete", args=(comment.pk,))


@parametrize_by_auth
def test_get(client: Client, *, auth: bool) -> None:
    if auth:
        auth_client(client)
    comment = factories.CommentFactory()
    with assert_count_diff(models.Comment, 0):
        response = client.get(get_url(comment))
    assert response.status_code == 405


def test_unauthed_post(client: Client) -> None:
    comment = factories.CommentFactory()
    with assert_count_diff(models.Comment, 0):
        response = client.post(get_url(comment), follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), get_url(comment)), 302)
    ]
    assert response.status_code == 200


def test_non_author_post(client: Client) -> None:
    user = auth_client(client)
    comment = factories.CommentFactory()
    with assert_count_diff(models.Comment, 0):
        response = client.post(get_url(comment), follow=True)
    assert response.redirect_chain == [(user.get_absolute_url(), 302)]
    assert response.status_code == 200


def test_author_post(client: Client) -> None:
    user = auth_client(client)
    comment = factories.CommentFactory(author=user)
    with assert_count_diff(models.Comment, -1):
        response = client.post(get_url(comment), follow=True)
    assert response.redirect_chain == [(user.get_absolute_url(), 302)]
    assert response.status_code == 200


def test_author_post_with_redirect(client: Client) -> None:
    user = auth_client(client)
    comment = factories.CommentFactory(author=user)
    post_url = comment.post.get_absolute_url()
    with assert_count_diff(models.Comment, -1):
        response = client.post(f"{get_url(comment)}?next={post_url}", follow=True)
    assert response.redirect_chain == [(post_url, 302)]
    assert response.status_code == 200
