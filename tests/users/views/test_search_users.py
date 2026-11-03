from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse_lazy

from tests.users.factories import UserFactory
from tests.utils import auth_client, parametrize_by_auth, set_image

if TYPE_CHECKING:
    from django.test import Client

url = reverse_lazy("users:search_users")


@parametrize_by_auth
@pytest.mark.parametrize(("q", "search_fields"), [(UserFactory.build().username, ["username"])])
def test_search_users(client: Client, *, auth: bool, q: str, search_fields: list[str]) -> None:
    if auth:
        auth_client(client)
    response = client.get(url, data={"q": q, "search_fields": search_fields})
    assert response.status_code == 200


def test_get_empty_form(client: Client) -> None:
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["users"] is None
    assert not response.context["form"].is_bound


def test_search_by_selected_fields(client: Client) -> None:
    found = UserFactory.create(location="Amsterdam", about="")
    UserFactory.create(location="Rotterdam", about="I like Amsterdam")
    response = client.get(url, data={"q": "Amsterdam", "search_fields": ["location"]})
    assert response.status_code == 200
    assert list(response.context["users"]) == [found]
    assert found.get_absolute_url() in response.content.decode()


def test_search_by_several_fields(client: Client) -> None:
    by_location = UserFactory.create(location="Amsterdam", about="")
    by_about = UserFactory.create(location="Rotterdam", about="I like Amsterdam")
    response = client.get(url, data={"q": "Amsterdam", "search_fields": ["location", "about"]})
    assert response.status_code == 200
    assert set(response.context["users"]) == {by_location, by_about}


def test_search_no_results(client: Client) -> None:
    UserFactory.create(location="Rotterdam")
    response = client.get(url, data={"q": "Amsterdam", "search_fields": ["location"]})
    assert response.status_code == 200
    assert not response.context["users"]
    assert "No users found." in response.content.decode()


def test_search_invalid_form(client: Client) -> None:
    response = client.get(url, data={"q": "Amsterdam"})
    assert response.status_code == 200
    assert response.context["users"] is None
    assert response.context["form"].errors == {"search_fields": ["This field is required."]}
    assert "No users found." not in response.content.decode()


def test_search_htmx_pagination(client: Client) -> None:
    users = UserFactory.create_batch(11, location="Amsterdam")
    data: dict[str, str | int | list[str]] = {"q": "Amsterdam", "search_fields": ["location"]}
    response = client.get(url, data=data)
    assert response.status_code == 200
    assert "hx-get=" in response.content.decode()
    response = client.get(url, data={**data, "page": 2}, headers={"hx-request": "true"})
    assert response.status_code == 200
    assert response.templates[0].name == "users/inc/search_users.html"
    [last] = response.context["users"]
    assert last in users
    assert "HX-Request" in response["Vary"]


def test_search_shows_image(client: Client) -> None:
    user = UserFactory.create(location="Amsterdam")
    image_src = set_image(user)
    response = client.get(url, data={"q": "Amsterdam", "search_fields": ["location"]})
    assert response.status_code == 200
    assert image_src in response.content.decode()
