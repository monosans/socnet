from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.template.defaultfilters import urlencode
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe

from tests.utils import auth_client

if TYPE_CHECKING:
    from django.test import Client

pytestmark = pytest.mark.parametrize(
    "url",
    (reverse_lazy("admin:index"), reverse_lazy("django-admindocs-docroot")),
)


def test_unauthed(client: Client, url: str) -> None:
    response = client.get(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("admin:login"), url), 302),
        (
            "{}?next={}".format(
                reverse("account_login"), urlencode(url, mark_safe(""))
            ),
            302,
        ),
    ]
    assert response.status_code == 200


def test_non_admin(client: Client, url: str) -> None:
    auth_client(client)
    response = client.get(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("admin:login"), url), 302)
    ]
    assert response.status_code == 403


def test_admin(admin_client: Client, url: str) -> None:
    response = admin_client.get(url)
    assert response.status_code == 200
