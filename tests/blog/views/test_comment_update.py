from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from socnet.blog import models
from tests.blog import factories
from tests.utils import ClientMethods, auth_client, parametrize_by_get_post

if TYPE_CHECKING:
    from typing import Any

    from django.test import Client

factory = factories.CommentFactory


def get_url(comment: models.Comment) -> str:
    return reverse("blog:comment_update", args=(comment.pk,))


@parametrize_by_get_post
def test_unauthed(client: Client, method: ClientMethods) -> None:
    comment = factory.create()
    url = get_url(comment)
    response = (
        client.get(url, follow=True)
        if method == ClientMethods.GET
        else client.post(url, follow=True)
    )
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("method", "data"),
    [
        (ClientMethods.GET, None),
        (ClientMethods.POST, None),
        (ClientMethods.POST, {"content": factory.build().content}),
    ],
)
def test_non_author(client: Client, method: ClientMethods, data: Any) -> None:
    auth_client(client)
    comment = factory.create()
    url = get_url(comment)
    response = (
        client.get(url)
        if method == ClientMethods.GET
        else client.post(url, data=data)
    )
    assert response.status_code == 403
    new_comment = models.Comment.objects.only("date_updated").get(pk=comment.pk)
    assert comment.date_updated == new_comment.date_updated


def test_author_get(client: Client) -> None:
    user = auth_client(client)
    comment = factory.create(author=user)
    url = get_url(comment)
    response = client.get(url)
    assert response.status_code == 200
    new_comment = models.Comment.objects.only("date_updated").get(pk=comment.pk)
    assert comment.date_updated == new_comment.date_updated


def test_author_post(client: Client) -> None:
    user = auth_client(client)
    comment = factory.create(author=user)
    url = get_url(comment)
    new_content = factory.build().content
    response = client.post(url, data={"content": new_content}, follow=True)
    assert response.redirect_chain == [
        (
            "{}#comment{}".format(
                reverse("blog:post", args=(comment.post.pk,)), comment.pk
            ),
            302,
        )
    ]
    assert response.status_code == 200
    updated_comment = models.Comment.objects.get(pk=comment.pk)
    assert updated_comment.author_id == comment.author_id
    assert updated_comment.content == new_content.strip()
    assert updated_comment.date_created == comment.date_created
    assert updated_comment.date_updated != comment.date_updated
    assert updated_comment.post_id == comment.post_id


def test_author_post_empty(client: Client) -> None:
    user = auth_client(client)
    comment = factory.create(author=user)
    url = get_url(comment)
    response = client.post(url)
    assert response.status_code == 200
    updated_comment = models.Comment.objects.only("date_updated").get(
        pk=comment.pk
    )
    assert updated_comment.date_updated == comment.date_updated
