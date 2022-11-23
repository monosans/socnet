from __future__ import annotations

from typing import Tuple

import pytest
from django.template.defaultfilters import urlencode
from django.test import Client
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe

from socnet.users.models import User

pytestmark = pytest.mark.django_db


class TestAdmin:
    url = reverse_lazy("admin:index")

    def test_unauthed(self, client: Client) -> None:
        response = client.get(self.url, follow=True)
        assert response.redirect_chain == [
            ("{}?next={}".format(reverse("admin:login"), self.url), 302),
            (
                "{}?next={}{}".format(
                    reverse("account_login"),
                    reverse("admin:login"),
                    urlencode(
                        "?next={}".format(urlencode(self.url, mark_safe(""))),
                        mark_safe(""),
                    ),
                ),
                302,
            ),
        ]
        assert response.status_code == 200

    def test_non_admin(self, authed_client: Client) -> None:
        response = authed_client.get(self.url, follow=True)
        assert response.redirect_chain == [
            ("{}?next={}".format(reverse("admin:login"), self.url), 302)
        ]
        assert response.status_code == 403

    def test_admin(self, admin_client: Client) -> None:
        response = admin_client.get(self.url)
        assert response.status_code == 200


class TestAdminDocs:
    url = reverse_lazy("django-admindocs-docroot")

    def test_unauthed(self, client: Client) -> None:
        response = client.get(self.url, follow=True)
        assert response.redirect_chain == [
            ("{}?next={}".format(reverse("admin:login"), self.url), 302),
            (
                "{}?next={}{}".format(
                    reverse("account_login"),
                    reverse("admin:login"),
                    urlencode(
                        "?next={}".format(urlencode(self.url, mark_safe(""))),
                        mark_safe(""),
                    ),
                ),
                302,
            ),
        ]
        assert response.status_code == 200

    def test_non_admin(self, authed_client: Client) -> None:
        response = authed_client.get(self.url, follow=True)
        assert response.redirect_chain == [
            ("{}?next={}".format(reverse("admin:login"), self.url), 302)
        ]
        assert response.status_code == 403

    def test_admin(self, admin_client: Client) -> None:
        response = admin_client.get(self.url)
        assert response.status_code == 200


class TestIndex:
    url = reverse_lazy("core:index")

    def test_unauthed(self, client: Client) -> None:
        response = client.get("", follow=True)
        assert response.redirect_chain == [
            ("{}?next={}".format(reverse("account_login"), self.url), 302)
        ]
        assert response.status_code == 200

    def test_authed(self, authed_client_user: Tuple[Client, User]) -> None:
        authed_client, user = authed_client_user
        response = authed_client.get(self.url, follow=True)
        assert response.redirect_chain == [(user.get_absolute_url(), 302)]
        assert response.status_code == 200


class TestRobotsTxt:
    url = "/robots.txt"

    def test_get(self, client: Client) -> None:
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/plain"

    def test_post(self, client: Client) -> None:
        response = client.post(self.url)
        assert response.status_code == 405
