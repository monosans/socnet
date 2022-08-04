from __future__ import annotations

import pytest
from django.test import Client


@pytest.mark.django_db
def test_unauthorized(client: Client) -> None:
    """Ensure that admin panel docs redirects to login."""
    response = client.get("/admin/doc/", follow=True)
    assert response.redirect_chain == [  # type: ignore[attr-defined]
        ("/admin/login/?next=/admin/doc/", 302),
        (
            "/accounts/login/?next=/admin/login/%3Fnext%3D%252Fadmin%252Fdoc%252F",
            302,
        ),
    ]
    assert response.status_code == 200


def test_authorized(authed_client: Client) -> None:
    """Ensure that admin panel docs access is forbidden for non-admins."""
    response = authed_client.get("/admin/doc", follow=True)
    assert response.redirect_chain == [  # type: ignore[attr-defined]
        ("/admin/login/?next=/admin/doc", 302)
    ]
    assert response.status_code == 403


def test_admin(admin_client: Client) -> None:
    """Ensure that admin panel docs is accessible for admins."""
    response = admin_client.get("/admin/doc/")
    assert response.status_code == 200
