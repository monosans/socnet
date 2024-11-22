from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse, reverse_lazy

from socnet.blog import models
from tests.blog import factories
from tests.utils import ClientMethods, auth_client, parametrize_by_get_post

if TYPE_CHECKING:
    from django.test import Client

factory = factories.PostFactory

url = reverse_lazy("blog:post_create")


@parametrize_by_get_post
def test_unauthed(client: Client, method: ClientMethods) -> None:
    response = (
        client.get(url, follow=True)
        if method == ClientMethods.GET
        else client.post(url, follow=True)
    )
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200
    assert not models.Post.objects.exists()


@parametrize_by_get_post
def test_authed(client: Client, method: ClientMethods) -> None:
    auth_client(client)
    response = (
        client.get(url) if method == ClientMethods.GET else client.post(url)
    )
    assert response.status_code == 200
    assert not models.Post.objects.exists()


def test_authed_post(client: Client) -> None:
    user = auth_client(client)
    content = factory.build().content
    response = client.post(url, data={"content": content}, follow=True)
    assert response.status_code == 200
    post = models.Post.objects.only("author_id", "content").last()
    assert post is not None
    assert response.redirect_chain == [(post.get_absolute_url(), 302)]
    assert post.author_id == user.pk
    assert post.content == content.strip()
