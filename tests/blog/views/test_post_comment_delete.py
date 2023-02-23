from __future__ import annotations

from django.test import Client
from django.urls import reverse

from socnet.blog import models

from ...conftest import AuthedClient
from ...utils import assert_count_diff
from .. import factories


def get_url(comment: models.PostComment) -> str:
    return reverse("blog:post_comment_delete", args=(comment.pk,))


def test_unauthed_get(client: Client) -> None:
    comment = factories.PostCommentFactory()
    with assert_count_diff(models.PostComment, 0):
        response = client.get(get_url(comment))
    assert response.status_code == 405


def test_authed_get(authed_client: AuthedClient) -> None:
    test_unauthed_get(authed_client.client)


def test_unauthed_post(client: Client) -> None:
    comment = factories.PostCommentFactory()
    with assert_count_diff(models.PostComment, 0):
        response = client.post(get_url(comment), follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), get_url(comment)), 302)
    ]
    assert response.status_code == 200


def test_non_author_post(authed_client: AuthedClient) -> None:
    client, user = authed_client
    comment = factories.PostCommentFactory()
    with assert_count_diff(models.PostComment, 0):
        response = client.post(get_url(comment), follow=True)
    assert response.redirect_chain == [(user.get_absolute_url(), 302)]
    assert response.status_code == 200


def test_author_post(authed_client: AuthedClient) -> None:
    client, user = authed_client
    comment = factories.PostCommentFactory(user=user)
    with assert_count_diff(models.PostComment, -1):
        response = client.post(get_url(comment), follow=True)
    assert response.redirect_chain == [(user.get_absolute_url(), 302)]
    assert response.status_code == 200


def test_author_post_with_redirect(authed_client: AuthedClient) -> None:
    client, user = authed_client
    comment = factories.PostCommentFactory(user=user)
    post_url = comment.post.get_absolute_url()
    with assert_count_diff(models.PostComment, -1):
        response = client.post(
            f"{get_url(comment)}?next={post_url}", follow=True
        )
    assert response.redirect_chain == [(post_url, 302)]
    assert response.status_code == 200
