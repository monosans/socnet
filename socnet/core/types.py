from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpRequest as HttpRequestBase

if TYPE_CHECKING:
    from django_htmx.middleware import HtmxDetails

    from socnet.users.models import User

    class HttpRequest(HttpRequestBase):
        htmx: HtmxDetails

    class AuthedRequest(HttpRequest):
        user: User

else:
    HttpRequest = HttpRequestBase
    AuthedRequest = HttpRequest
