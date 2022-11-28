from __future__ import annotations

# pylint: disable-next=no-name-in-module
from abc import ABCMeta, abstractmethod
from typing import Tuple

import pytest
from django.test import Client
from django.urls import reverse, reverse_lazy

from socnet.blog import models
from socnet.users.models import User

from ..test_users.factories import UserFactory
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

    def test_authed_post(
        self, authed_client_user: Tuple[Client, User]
    ) -> None:
        authed_client, user = authed_client_user
        text = "post_text"
        with assert_count_diff(models.Post, 1):
            response = authed_client.post(
                self.url, data={"text": text}, follow=True
            )
        assert response.status_code == 200
        post = models.Post.objects.order_by("-pk").get()
        assert post.user == user
        assert post.text == text
        assert response.redirect_chain == [(post.get_absolute_url(), 302)]


class TestPostCommentDelete:
    def get_url(self, comment: models.PostComment) -> str:
        return reverse("blog:post_comment_delete", args=(comment.pk,))

    def test_unauthed_get(self, client: Client) -> None:
        comment = factories.PostCommentFactory()
        with assert_count_diff(models.PostComment, 0):
            response = client.get(self.get_url(comment))
        assert response.status_code == 405

    def test_authed_get(self, authed_client: Client) -> None:
        self.test_unauthed_get(authed_client)

    def test_unauthed_post(self, client: Client) -> None:
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

    def test_non_author_post(
        self, authed_client_user: Tuple[Client, User]
    ) -> None:
        authed_client, user = authed_client_user
        comment = factories.PostCommentFactory()
        with assert_count_diff(models.PostComment, 0):
            response = authed_client.post(self.get_url(comment), follow=True)
        assert response.redirect_chain == [(user.get_absolute_url(), 302)]
        assert response.status_code == 200

    def test_author_post(
        self, authed_client_user: Tuple[Client, User]
    ) -> None:
        authed_client, user = authed_client_user
        comment = factories.PostCommentFactory(user=user)
        with assert_count_diff(models.PostComment, -1):
            response = authed_client.post(self.get_url(comment), follow=True)
        assert response.redirect_chain == [(user.get_absolute_url(), 302)]
        assert response.status_code == 200

    def test_author_post_with_redirect(
        self, authed_client_user: Tuple[Client, User]
    ) -> None:
        authed_client, user = authed_client_user
        comment = factories.PostCommentFactory(user=user)
        post_url = comment.post.get_absolute_url()
        with assert_count_diff(models.PostComment, -1):
            response = authed_client.post(
                f"{self.get_url(comment)}?next={post_url}", follow=True
            )
        assert response.redirect_chain == [(post_url, 302)]
        assert response.status_code == 200


class TestPostDelete:
    def get_url(self, post: models.Post) -> str:
        return reverse("blog:post_delete", args=(post.pk,))

    def test_unauthed_get(self, client: Client) -> None:
        post = factories.PostFactory()
        with assert_count_diff(models.Post, 0):
            response = client.get(self.get_url(post))
        assert response.status_code == 405

    def test_authed_get(self, authed_client: Client) -> None:
        self.test_unauthed_get(authed_client)

    def test_unauthed_post(self, client: Client) -> None:
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

    def test_author_post(
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

    def test_non_author_post(
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


class TestPost:
    def get_url(self, post: models.Post) -> str:
        return reverse("blog:post", args=(post.pk,))

    def test_unauthed_get(self, client: Client) -> None:
        post = factories.PostFactory()
        with assert_count_diff(models.PostComment, 0):
            response = client.get(self.get_url(post))
        assert response.status_code == 200

    def test_authed_get(self, authed_client: Client) -> None:
        self.test_unauthed_get(authed_client)

    def test_unauthed_post(self, client: Client) -> None:
        post = factories.PostFactory()
        url = self.get_url(post)
        with assert_count_diff(models.PostComment, 0):
            response = client.post(url, follow=True)
        assert response.redirect_chain == [
            ("{}?next={}".format(reverse("account_login"), url), 302)
        ]
        assert response.status_code == 200

    def test_authed_post(
        self, authed_client_user: Tuple[Client, User]
    ) -> None:
        authed_client, user = authed_client_user
        post = factories.PostFactory()
        text = "comment text"
        with assert_count_diff(models.PostComment, 1):
            response = authed_client.post(
                self.get_url(post), data={"text": text}
            )
        assert response.status_code == 200
        comment = models.PostComment.objects.order_by("-pk").get()
        assert comment.user == user
        assert comment.text == text

    def test_authed_post_empty(self, authed_client: Client) -> None:
        post = factories.PostFactory()
        with assert_count_diff(models.PostComment, 0):
            response = authed_client.post(self.get_url(post))
        assert response.status_code == 200


class TestPosts:
    url = reverse_lazy("blog:posts")

    def test_unauthed_get(self, client: Client) -> None:
        response = client.get(self.url)
        assert response.status_code == 200

    def test_authed_get(self, authed_client: Client) -> None:
        self.test_unauthed_get(authed_client)

    def test_unauthed_get_search(self, client: Client) -> None:
        response = client.get(f"{self.url}?q=query")
        assert response.status_code == 200

    def test_unauthed_get_search_empty_q(self, client: Client) -> None:
        response = client.get(f"{self.url}?q=")
        assert response.status_code == 200

    def test_authed_get_search(self, authed_client: Client) -> None:
        self.test_unauthed_get_search(authed_client)

    def test_unauthed_post(self, client: Client) -> None:
        response = client.post(self.url)
        assert response.status_code == 405

    def test_authed_post(self, authed_client: Client) -> None:
        response = authed_client.post(self.url)
        assert response.status_code == 405


class ABCUserTest(metaclass=ABCMeta):
    @property
    @abstractmethod
    def viewname(self) -> str:
        pass

    def get_url(self, user: User) -> str:
        return reverse(self.viewname, args=(user.get_username(),))

    def test_unauthed_get(self, client: Client) -> None:
        user = UserFactory()
        response = client.get(self.get_url(user))
        assert response.status_code == 200

    def test_authed_get(self, authed_client: Client) -> None:
        self.test_unauthed_get(authed_client)

    def test_unauthed_post(self, client: Client) -> None:
        user = UserFactory()
        response = client.post(self.get_url(user))
        assert response.status_code == 405

    def test_authed_post(self, authed_client: Client) -> None:
        self.test_unauthed_post(authed_client)


class TestLikedPosts(ABCUserTest):
    @property
    def viewname(self) -> str:
        return "blog:liked_posts"


class TestUserPosts(ABCUserTest):
    @property
    def viewname(self) -> str:
        return "blog:user_posts"


class TestSubscribers(ABCUserTest):
    @property
    def viewname(self) -> str:
        return "blog:subscribers"


class TestSubscriptions(ABCUserTest):
    @property
    def viewname(self) -> str:
        return "blog:subscriptions"


class TestUser(ABCUserTest):
    @property
    def viewname(self) -> str:
        return "blog:user"
