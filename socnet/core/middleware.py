from __future__ import annotations

from django.http.request import HttpRequest
from django.http.response import HttpResponseBase
from django.utils.deprecation import MiddlewareMixin

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
