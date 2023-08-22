from __future__ import annotations

import django_minify_html.middleware
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


class MinifyHtmlMiddleware(django_minify_html.middleware.MinifyHtmlMiddleware):
    minify_args = {
        "do_not_minify_doctype": True,
        "ensure_spec_compliant_unquoted_attribute_values": True,
        "minify_css": True,
        "minify_js": True,
    }
