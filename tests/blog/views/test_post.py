from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from socnet.blog import models
from tests.blog import factories
from tests.utils import ClientMethods, auth_client, set_image

if TYPE_CHECKING:
    from django.test import Client

factory = factories.PostFactory


def get_url(post: models.Post) -> str:
    return reverse("blog:post", args=(post.pk,))


@pytest.mark.parametrize(
    ("auth", "method"),
    [(False, ClientMethods.GET), (True, ClientMethods.GET), (True, ClientMethods.POST)],
)
def test_empty_request(client: Client, *, auth: bool, method: ClientMethods) -> None:
    if auth:
        auth_client(client)
    post = factory.create()
    url = get_url(post)
    response = client.get(url) if method == ClientMethods.GET else client.post(url)
    assert response.status_code == 200
    assert not models.Comment.objects.exists()


def test_unauthed_post(client: Client) -> None:
    post = factory.create()
    url = get_url(post)
    response = client.post(url, follow=True)
    assert response.redirect_chain == [("{}?next={}".format(reverse("account_login"), url), 302)]
    assert response.status_code == 200
    assert not models.Comment.objects.exists()


def test_authed_post(client: Client) -> None:
    user = auth_client(client)
    post = factory.create()
    url = get_url(post)
    comment_content = factories.CommentFactory.build().content
    response = client.post(url, data={"content": comment_content}, follow=True)
    assert response.status_code == 200
    comment = models.Comment.objects.only("author_id", "content", "post_id").last()
    assert comment is not None
    assert response.redirect_chain == [(url, 302)]
    assert comment.author_id == user.pk
    assert comment.content == comment_content.strip()
    assert comment.post_id == post.pk


def test_missing_post(client: Client) -> None:
    assert client.get(reverse("blog:post", args=(1,))).status_code == 404


def test_comment_on_missing_post(client: Client) -> None:
    auth_client(client)
    url = reverse("blog:post", args=(1,))
    response = client.post(url, data={"content": "content"})
    assert response.status_code == 404
    assert not models.Comment.objects.exists()


def test_commenting_restricted(client: Client) -> None:
    auth_client(client)
    post = factory.create(allow_commenting=False)
    url = get_url(post)
    response = client.get(url)
    assert response.status_code == 200
    assert "The author has restricted commenting on this post." in response.content.decode()
    response = client.post(url, data={"content": "content"})
    assert response.status_code == 200
    assert [str(m) for m in response.context["messages"]] == [
        "An error occurred while creating the comment. Please try again."
    ]
    assert not models.Comment.objects.exists()


def test_author_can_comment_when_restricted(client: Client) -> None:
    user = auth_client(client)
    post = factory.create(author=user, allow_commenting=False)
    url = get_url(post)
    response = client.get(url)
    assert response.status_code == 200
    assert "The author has restricted commenting on this post." not in response.content.decode()
    response = client.post(url, data={"content": "content"}, follow=True)
    assert response.redirect_chain == [(url, 302)]
    comment = models.Comment.objects.get()
    assert comment.author_id == user.pk
    assert comment.post_id == post.pk


def test_unauthed_get_asks_to_log_in(client: Client) -> None:
    post = factory.create()
    url = get_url(post)
    response = client.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    assert "{}?next={}".format(reverse("account_login"), url) in content
    assert 'method="post"' not in content


def test_controls_for_author(client: Client) -> None:
    user = auth_client(client)
    post = factory.create(author=user)
    response = client.get(get_url(post))
    assert response.status_code == 200
    content = response.content.decode()
    assert reverse("blog:post_update", args=(post.pk,)) in content
    assert reverse("blog:post_delete", args=(post.pk,)) in content
    assert reverse("admin:blog_post_change", args=(post.pk,)) not in content


def test_controls_for_staff(admin_client: Client) -> None:
    post = factory.create()
    response = admin_client.get(get_url(post))
    assert response.status_code == 200
    content = response.content.decode()
    assert reverse("admin:blog_post_change", args=(post.pk,)) in content
    assert reverse("blog:post_update", args=(post.pk,)) not in content
    assert reverse("blog:post_delete", args=(post.pk,)) not in content


def test_author_image(client: Client) -> None:
    post = factory.create()
    image_src = set_image(post.author)
    response = client.get(get_url(post))
    assert response.status_code == 200
    assert image_src in response.content.decode()
