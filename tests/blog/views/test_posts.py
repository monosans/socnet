from __future__ import annotations

import pytest
from django.test import Client
from django.urls import reverse_lazy

from ...utils import auth_client, parametrize_by_auth

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
