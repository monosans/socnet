from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from socnet.blog import db_utils
from tests.utils import auth_client

if TYPE_CHECKING:
    from typing import NoReturn


def test_not_found(client: Client) -> None:
    response = client.get("/does-not-exist/")
    assert response.status_code == 404
    assert response.templates[0].name == "404.html"
    assert "Not Found (404)" in response.content.decode()


def test_csrf_failure() -> None:
    client = Client(enforce_csrf_checks=True)
    auth_client(client)
    response = client.post(reverse("blog:post_create"), data={"content": "content"})
    assert response.status_code == 403
    assert response.templates[0].name == "403_csrf.html"
    assert "CSRF verification failed (403)" in response.content.decode()


def test_too_many_requests(client: Client) -> None:
    url = reverse("account_signup")
    # allauth allows 20 sign-up attempts a minute from the same IP address.
    for _ in range(20):
        assert client.post(url).status_code == 200
    response = client.post(url)
    assert response.status_code == 429
    assert response.templates[0].name == "429.html"
    assert "Too Many Requests (429)" in response.content.decode()


# Django renders 500.html without a request, so the template sees no csrf_token.
@pytest.mark.ignore_template_errors
def test_server_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(*_args: object, **_kwargs: object) -> NoReturn:
        raise RuntimeError

    monkeypatch.setattr(db_utils, "get_posts_preview_qs", fail)
    client = Client(raise_request_exception=False)
    response = client.get(reverse("blog:posts"))
    assert response.status_code == 500
    assert "Internal Server Error (500)" in response.content.decode()
