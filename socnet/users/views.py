from __future__ import annotations

from typing import Any

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect

from .types import AuthedRequest


@login_required
def admin_site_login_view(
    request: AuthedRequest,
    # pylint: disable-next=unused-argument
    extra_context: dict[str, Any] | None = None,
) -> HttpResponse:
    if not admin.site.has_permission(request):
        raise PermissionDenied
    next_page = request.GET.get("next", "admin:index")
    return redirect(next_page)
