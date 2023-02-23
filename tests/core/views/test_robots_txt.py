from __future__ import annotations

from django.test import Client

url = "/robots.txt"


def test_get(client: Client) -> None:
    response = client.get(url)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain"


def test_post(client: Client) -> None:
    response = client.post(url)
    assert response.status_code == 405
