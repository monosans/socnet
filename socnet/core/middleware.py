from __future__ import annotations

from typing import TYPE_CHECKING

from django.utils.deprecation import MiddlewareMixin

import socnet_rs

if TYPE_CHECKING:
    from django.http import HttpResponse
    from django.http.response import HttpResponseBase

    from socnet.core.types import HttpRequest

HEADERS = (
    (
        "Content-Security-Policy",
        (
            "default-src 'none'; "
            "connect-src 'self'; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' blob: data: https:;"
        ),
    ),
    ("Permissions-Policy", "interest-cohort=()"),
    ("Referrer-Policy", "same-origin"),
    ("X-Content-Type-Options", "nosniff"),
    ("X-Frame-Options", "DENY"),
)


class ResponseHeadersMiddleware(MiddlewareMixin):
    def process_response(  # noqa: PLR6301
        self,
        request: HttpRequest,  # noqa: ARG002
        response: HttpResponseBase,
    ) -> HttpResponseBase:
        for header, value in HEADERS:
            response.headers.setdefault(header, value)
        return response


class MinifyHtmlMiddleware(MiddlewareMixin):
    """Based on https://github.com/adamchainz/django-minify-html"""

    def process_response(  # noqa: PLR6301
        self,
        request: HttpRequest,  # noqa: ARG002
        response: HttpResponseBase,
    ) -> HttpResponseBase:
        if (
            not getattr(response, "streaming", False)
            and response.get("Content-Encoding", "") == ""  # noqa: PLC1901
            and response.get("Content-Type", "").split(";", 1)[0] == "text/html"
        ):
            if TYPE_CHECKING:
                assert isinstance(response, HttpResponse)
            content = response.content.decode(response.charset)
            minified_content = socnet_rs.minify_html(content)
            response.content = minified_content
            if "Content-Length" in response:
                response["Content-Length"] = len(response.content)
        return response
