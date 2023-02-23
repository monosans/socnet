from __future__ import annotations

from django.test import Client
from django.urls import reverse_lazy

from ...conftest import AuthedClient

url = reverse_lazy("blog:posts")


def test_unauthed_get(client: Client) -> None:
    response = client.get(url)
    assert response.status_code == 200


def test_authed_get(authed_client: AuthedClient) -> None:
    test_unauthed_get(authed_client.client)


def test_unauthed_get_search(client: Client) -> None:
    response = client.get(f"{url}?q=query")
    assert response.status_code == 200


def test_unauthed_get_search_empty_q(client: Client) -> None:
    response = client.get(f"{url}?q=")
    assert response.status_code == 200


def test_authed_get_search(authed_client: AuthedClient) -> None:
    test_unauthed_get_search(authed_client.client)


def test_unauthed_post(client: Client) -> None:
    response = client.post(url)
    assert response.status_code == 405


def test_authed_post(authed_client: AuthedClient) -> None:
    test_unauthed_post(authed_client.client)
