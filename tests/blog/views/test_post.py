from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from socnet.blog import models
from tests.blog import factories
from tests.utils import ClientMethods, auth_client

if TYPE_CHECKING:
    from django.test import Client

factory = factories.PostFactory


def get_url(post: models.Post) -> str:
    return reverse("blog:post", args=(post.pk,))


@pytest.mark.parametrize(
    ("auth", "method"),
    [
        (False, ClientMethods.GET),
        (True, ClientMethods.GET),
        (True, ClientMethods.POST),
    ],
)
def test_empty_request(
    client: Client, *, auth: bool, method: ClientMethods
) -> None:
    if auth:
        auth_client(client)
    post = factory.create()
    url = get_url(post)
    response = (
        client.get(url) if method == ClientMethods.GET else client.post(url)
    )
    assert response.status_code == 200
    assert not models.Comment.objects.exists()


def test_unauthed_post(client: Client) -> None:
    post = factory.create()
    url = get_url(post)
    response = client.post(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200
    assert not models.Comment.objects.exists()


def test_authed_post(client: Client) -> None:
    user = auth_client(client)
    post = factory.create()
    url = get_url(post)
    comment_content = factories.CommentFactory.build().content
    response = client.post(url, data={"content": comment_content}, follow=True)
    assert response.status_code == 200
    comment = models.Comment.objects.only(
        "author_id", "content", "post_id"
    ).last()
    assert comment is not None
    assert response.redirect_chain == [(url, 302)]
    assert comment.author_id == user.pk
    assert comment.content == comment_content.strip()
    assert comment.post_id == post.pk
