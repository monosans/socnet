from __future__ import annotations

from typing import Any, Dict, Optional

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from ..users.types import AuthedRequest


@login_required
def admin_site_login_view(
    request: AuthedRequest,
    extra_context: Optional[Dict[str, Any]] = None,  # noqa: ARG001
) -> HttpResponse:
    if not admin.site.has_permission(request):
        raise PermissionDenied
    redirect_to = request.GET.get("next", "admin:index")
    return redirect(redirect_to)


@login_required
def index_view(request: AuthedRequest) -> HttpResponse:
    return redirect(request.user)


class ManifestView(TemplateView):
    template_name = "site.webmanifest"
    content_type = "application/json"
