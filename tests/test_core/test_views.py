from __future__ import annotations

from typing import Tuple

import pytest
from django.test import Client

from socnet.users.models import User


class TestAdmin:
    @pytest.mark.django_db
    def test_unauthed(self, client: Client) -> None:
        """Ensure that admin panel redirects to login."""
        response = client.get("/admin/", follow=True)
        assert response.redirect_chain == [
            ("/admin/login/?next=/admin/", 302),
            ("/login/?next=/admin/login/%3Fnext%3D%252Fadmin%252F", 302),
        ]
        assert response.status_code == 200

    def test_authed(self, authed_client: Client) -> None:
        """Ensure that admin panel access is forbidden for non-admins."""
        response = authed_client.get("/admin/", follow=True)
        assert response.redirect_chain == [("/admin/login/?next=/admin/", 302)]
        assert response.status_code == 403

    def test_admin(self, admin_client: Client) -> None:
        """Ensure that admin panel is accessible for admins."""
        response = admin_client.get("/admin/")
        assert response.status_code == 200


class TestAdminDocs:
    @pytest.mark.django_db
    def test_unauthed(self, client: Client) -> None:
        """Ensure that admin panel docs redirects to login."""
        response = client.get("/admin/doc/", follow=True)
        assert response.redirect_chain == [
            ("/admin/login/?next=/admin/doc/", 302),
            (
                "/login/?next=/admin/login/%3Fnext%3D%252Fadmin%252Fdoc%252F",
                302,
            ),
        ]
        assert response.status_code == 200

    def test_authed(self, authed_client: Client) -> None:
        """Ensure that admin panel docs access is forbidden for non-admins."""
        response = authed_client.get("/admin/doc", follow=True)
        assert response.redirect_chain == [
            ("/admin/login/?next=/admin/doc", 302)
        ]
        assert response.status_code == 403

    def test_admin(self, admin_client: Client) -> None:
        """Ensure that admin panel docs is accessible for admins."""
        response = admin_client.get("/admin/doc/")
        assert response.status_code == 200


class TestIndex:
    @pytest.mark.django_db
    def test_unauthed(self, client: Client) -> None:
        response = client.get("", follow=True)
        assert response.redirect_chain == [("/login/?next=/", 302)]
        assert response.status_code == 200

    def test_authed(self, authed_client_user: Tuple[Client, User]) -> None:
        client, user = authed_client_user
        response = client.get("", follow=True)
        assert response.redirect_chain == [
            (f"/user/{user.get_username()}/", 302)
        ]
        assert response.status_code == 200


class TestRobotsTxt:
    @pytest.mark.django_db
    def test_get(self, client: Client) -> None:
        response = client.get("/robots.txt")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/plain"

    @pytest.mark.django_db
    def test_post(self, client: Client) -> None:
        response = client.post("/robots.txt")
        assert response.status_code == 405
