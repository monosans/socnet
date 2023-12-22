from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.templatetags.static import static
from django.views.generic import TemplateView
from typing_extensions import Any

from ..users.types import AuthedRequest


@login_required
def admin_site_login_view(
    request: AuthedRequest,
    extra_context: dict[str, Any] | None = None,  # noqa: ARG001
) -> HttpResponse:
    if not admin.site.has_permission(request):
        raise PermissionDenied
    redirect_to = request.GET.get("next", "admin:index")
    return redirect(redirect_to)


@login_required
def index_view(request: AuthedRequest) -> HttpResponse:
    return redirect(request.user)


def favicon_view(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    return redirect(static("img/favicon.ico"))


class ManifestView(TemplateView):
    template_name = "site.webmanifest"
    content_type = "application/json"
