from __future__ import annotations

from django.test import Client
from django.urls import reverse, reverse_lazy

from ...conftest import AuthedClient

url = reverse_lazy("core:index")


def test_unauthed(client: Client) -> None:
    response = client.get("", follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
    assert response.status_code == 200


def test_authed(authed_client: AuthedClient) -> None:
    client, user = authed_client
    response = client.get(url, follow=True)
    assert response.redirect_chain == [(user.get_absolute_url(), 302)]
    assert response.status_code == 200
