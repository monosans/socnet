from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect

from .types import AuthedRequest


@login_required
def admin_site_login_view(request: AuthedRequest) -> HttpResponse:
    if not request.user.is_staff:
        raise PermissionDenied
    next = request.GET.get("next", "admin:index")
    return redirect(next)
