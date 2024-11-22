from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse, reverse_lazy

from tests.utils import auth_client

if TYPE_CHECKING:
    from django.test import Client

url = reverse_lazy("users:account_security")


def test_unauthed_get(client: Client) -> None:
    response = client.get(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200


def test_authed_get(client: Client) -> None:
    auth_client(client)
    response = client.get(url)
    assert response.status_code == 200
