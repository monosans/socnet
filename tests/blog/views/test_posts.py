from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse_lazy

from tests.utils import auth_client, parametrize_by_auth

if TYPE_CHECKING:
    from django.test import Client

url = reverse_lazy("blog:posts")


@parametrize_by_auth
def test_unauthed_get(client: Client, *, auth: bool) -> None:
    if auth:
        auth_client(client)
    response = client.get(url)
    assert response.status_code == 200


@parametrize_by_auth
@pytest.mark.parametrize("q", ["query", ""])
def test_get_search(client: Client, *, auth: bool, q: str) -> None:
    if auth:
        auth_client(client)
    response = client.get(f"{url}?q={q}")
    assert response.status_code == 200
