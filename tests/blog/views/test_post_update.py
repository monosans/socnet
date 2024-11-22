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

factory = factories.PostFactory


def get_url(post: models.Post) -> str:
    return reverse("blog:post_update", args=(post.pk,))


@parametrize_by_get_post
def test_unauthed(client: Client, method: ClientMethods) -> None:
    post = factory()
    url = get_url(post)
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
    post = factory()
    url = get_url(post)
    response = (
        client.get(url)
        if method == ClientMethods.GET
        else client.post(url, data=data)
    )
    assert response.status_code == 403
    new_post = models.Post.objects.only("date_updated").get(pk=post.pk)
    assert post.date_updated == new_post.date_updated


def test_author_get(client: Client) -> None:
    user = auth_client(client)
    post = factory(author=user)
    url = get_url(post)
    response = client.get(url)
    assert response.status_code == 200
    new_post = models.Post.objects.only("date_updated").get(pk=post.pk)
    assert post.date_updated == new_post.date_updated


def test_author_post(client: Client) -> None:
    user = auth_client(client)
    post = factory(author=user)
    url = get_url(post)
    new_content = factory.build().content
    response = client.post(url, data={"content": new_content}, follow=True)
    assert response.redirect_chain == [
        (reverse("blog:post", args=(post.pk,)), 302)
    ]
    assert response.status_code == 200
    updated_post = models.Post.objects.get(pk=post.pk)
    assert updated_post.author_id == post.author_id
    assert updated_post.content == new_content.strip()
    assert updated_post.date_created == post.date_created
    assert updated_post.date_updated != post.date_updated


def test_author_post_empty(client: Client) -> None:
    user = auth_client(client)
    post = factory(author=user)
    url = get_url(post)
    response = client.post(url)
    assert response.status_code == 200
    updated_comment = models.Post.objects.only("date_updated").get(pk=post.pk)
    assert updated_comment.date_updated == post.date_updated
