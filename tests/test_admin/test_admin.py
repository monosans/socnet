from __future__ import annotations

import pytest
from django.test import Client


@pytest.mark.django_db
def test_unauthrozied(client: Client) -> None:
    """Ensure that admin panel redirects to login."""
    response = client.get("/admin/")
    assert response.status_code == 302


def test_authorized(authed_client: Client) -> None:
    """Ensure that admin panel access is forbidden for non-admins."""
    response = authed_client.get("/admin/", follow=True)
    assert response.status_code == 403


def test_admin(admin_client: Client) -> None:
    """Ensure that admin panel is accessible for admins."""
    response = admin_client.get("/admin/")
    assert response.status_code == 200
