from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponseBase
from django.utils.deprecation import MiddlewareMixin

import socnet_rs

HEADERS = (
    (
        "Content-Security-Policy",
        (
            "default-src 'none'; "
            "connect-src 'self'; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:;"
        ),
    ),
    ("Permissions-Policy", "interest-cohort=()"),
    ("Referrer-Policy", "same-origin"),
    ("X-Content-Type-Options", "nosniff"),
    ("X-Frame-Options", "DENY"),
)


class ResponseHeadersMiddleware(MiddlewareMixin):
    def process_response(
        self, request: HttpRequest, response: HttpResponseBase  # noqa: ARG002
    ) -> HttpResponseBase:
        for header, value in HEADERS:
            response.headers.setdefault(header, value)
        return response


class MinifyHtmlMiddleware(MiddlewareMixin):
    """Based on https://github.com/adamchainz/django-minify-html."""

    def process_response(
        self, request: HttpRequest, response: HttpResponseBase  # noqa: ARG002
    ) -> HttpResponseBase:
        if (
            not getattr(response, "streaming", False)
            and response.get("Content-Encoding", "") == ""
            and response.get("Content-Type", "").split(";", 1)[0] == "text/html"
        ):
            if TYPE_CHECKING:
                assert isinstance(response, HttpResponse)
            content = response.content.decode(response.charset)
            minified_content = socnet_rs.minify_html(content)
            response.content = minified_content
            if "Content-Length" in response:
                response["Content-Length"] = len(minified_content)
        return response
