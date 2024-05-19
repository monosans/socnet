from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.templatetags.static import static
from django.views.generic import TemplateView

from ..users.types import AuthedRequest


@login_required
def index_view(request: AuthedRequest) -> HttpResponse:
    return redirect(request.user)


def favicon_view(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    return redirect(static("img/favicon.ico"))


class ManifestView(TemplateView):
    template_name = "site.webmanifest"
    content_type = "application/json"
