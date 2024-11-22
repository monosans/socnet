from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse_lazy

from tests.users.factories import UserFactory
from tests.utils import auth_client, parametrize_by_auth

if TYPE_CHECKING:
    from django.test import Client

url = reverse_lazy("users:search_users")


@parametrize_by_auth
@pytest.mark.parametrize(
    ("q", "search_fields"), [(UserFactory.build().username, ["username"])]
)
def test_search_users(
    client: Client, *, auth: bool, q: str, search_fields: list[str]
) -> None:
    if auth:
        auth_client(client)
    response = client.get(url, data={"q": q, "search_fields": search_fields})
    assert response.status_code == 200
