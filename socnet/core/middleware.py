from __future__ import annotations

from typing import TYPE_CHECKING

from django.utils.deprecation import MiddlewareMixin

if TYPE_CHECKING:
    from django.http.response import HttpResponseBase

    from socnet.core.types import HttpRequest

HEADERS = (
    (
        "Content-Security-Policy",
        (
            "default-src 'none'; "
            "base-uri 'self'; "
            "connect-src 'self'; "
            "font-src 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' blob: data:; "
            "manifest-src 'self';"
        ),
    ),
    ("Cross-Origin-Opener-Policy", "same-origin"),
    ("Permissions-Policy", "camera=(), geolocation=(), microphone=()"),
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
