from __future__ import annotations

import pytest
from django.test import Client


@pytest.mark.django_db
def test_robots_txt(client: Client) -> None:
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain"
