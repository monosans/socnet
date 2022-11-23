from __future__ import annotations

from typing import Tuple

import pytest
from django.test import Client
from django.urls import reverse_lazy, reverse
from socnet.blog import models
from socnet.users.models import User

from ..utils import assert_count_diff
from . import factories

pytestmark = pytest.mark.django_db


class TestCreatePost:
    url = reverse_lazy("blog:create_post")

    def test_unauthed_get(self, client: Client) -> None:
        with assert_count_diff(models.Post, 0):
            response = client.get(self.url, follow=True)
            assert response.redirect_chain == [
                ("{}?next={}".format(reverse("account_login"), self.url), 302)
            ]
            assert response.status_code == 200

    def test_unauthed_post(self, client: Client) -> None:
        with assert_count_diff(models.Post, 0):
            response = client.post(self.url, follow=True)
            assert response.redirect_chain == [
                ("{}?next={}".format(reverse("account_login"), self.url), 302)
            ]
            assert response.status_code == 200

    def test_authed_get(self, authed_client: Client) -> None:
        with assert_count_diff(models.Post, 0):
            response = authed_client.get(self.url)
            assert response.status_code == 200

    def test_authed_post_empty(self, authed_client: Client) -> None:
        with assert_count_diff(models.Post, 0):
            response = authed_client.post(self.url)
            assert response.status_code == 200

    def test_authed_post(self, authed_client: Client) -> None:
        with assert_count_diff(models.Post, 1):
            response = authed_client.post(
                self.url, data={"text": "post text"}, follow=True
            )
            post = models.Post.objects.order_by("-pk").get()
            assert post.text == "post text"
            assert response.redirect_chain == [(post.get_absolute_url(), 302)]
            assert response.status_code == 200


class TestPostCommentDelete:
    def get_url(self, comment: models.PostComment) -> str:
        return reverse("blog:post_comment_delete", args=(comment.pk,))

    def test_get(self, client: Client) -> None:
        comment = factories.PostCommentFactory()
        with assert_count_diff(models.PostComment, 0):
            response = client.get(self.get_url(comment))
            assert response.status_code == 405

    def test_post_unauthed(self, client: Client) -> None:
        comment = factories.PostCommentFactory()
        with assert_count_diff(models.PostComment, 0):
            response = client.post(self.get_url(comment), follow=True)
            assert response.redirect_chain == [
                (
                    "{}?next={}".format(
                        reverse("account_login"), self.get_url(comment)
                    ),
                    302,
                )
            ]
            assert response.status_code == 200

    def test_post_author(
        self, authed_client_user: Tuple[Client, User]
    ) -> None:
        authed_client, user = authed_client_user
        comment = factories.PostCommentFactory(user=user)
        with assert_count_diff(models.PostComment, -1):
            response = authed_client.post(self.get_url(comment), follow=True)
            assert response.redirect_chain == [(user.get_absolute_url(), 302)]
            assert response.status_code == 200

    def test_post_not_author(
        self, authed_client_user: Tuple[Client, User]
    ) -> None:
        authed_client, user = authed_client_user
        comment = factories.PostCommentFactory()
        with assert_count_diff(models.PostComment, 0):
            response = authed_client.post(self.get_url(comment), follow=True)
            assert response.redirect_chain == [(user.get_absolute_url(), 302)]
            assert response.status_code == 200

    def test_post_author_with_redirect(
        self, authed_client_user: Tuple[Client, User]
    ) -> None:
        authed_client, user = authed_client_user
        comment = factories.PostCommentFactory(user=user)
        post_url = comment.post.get_absolute_url()
        with assert_count_diff(models.PostComment, -1):
            response = authed_client.post(
                "{}?next={}".format(self.get_url(comment), post_url),
                follow=True,
            )
            assert response.redirect_chain == [(post_url, 302)]
            assert response.status_code == 200


class TestPostDelete:
    def get_url(self, post: models.Post) -> str:
        return reverse("blog:post_delete", args=(post.pk,))

    def test_get(self, client: Client) -> None:
        post = factories.PostFactory()
        with assert_count_diff(models.Post, 0):
            response = client.get(self.get_url(post))
            assert response.status_code == 405

    def test_post_unauthed(self, client: Client) -> None:
        post = factories.PostFactory()
        with assert_count_diff(models.Post, 0):
            response = client.post(self.get_url(post), follow=True)
            assert response.redirect_chain == [
                (
                    "{}?next={}".format(
                        reverse("account_login"), self.get_url(post)
                    ),
                    302,
                )
            ]
            assert response.status_code == 200

    def test_post_author(
        self, authed_client_user: Tuple[Client, User]
    ) -> None:
        authed_client, user = authed_client_user
        post = factories.PostFactory(user=user)
        with assert_count_diff(models.Post, -1):
            response = authed_client.post(self.get_url(post), follow=True)
            assert response.redirect_chain == [
                (reverse("blog:user_posts", args=(user.get_username(),)), 302)
            ]
            assert response.status_code == 200

    def test_post_not_author(
        self, authed_client_user: Tuple[Client, User]
    ) -> None:
        authed_client, user = authed_client_user
        post = factories.PostFactory()
        with assert_count_diff(models.Post, 0):
            response = authed_client.post(self.get_url(post), follow=True)
            assert response.redirect_chain == [
                (reverse("blog:user_posts", args=(user.get_username(),)), 302)
            ]
            assert response.status_code == 200
