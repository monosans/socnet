from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.templatetags.static import static
from django.views.generic import TemplateView

if TYPE_CHECKING:
    from django.http import HttpResponse

    from socnet.core.types import AuthedRequest, HttpRequest


@login_required
def index_view(request: AuthedRequest) -> HttpResponse:
    return redirect(request.user)


def favicon_view(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    return redirect(static("img/favicon.ico"))


class ManifestView(TemplateView):
    template_name = "site.webmanifest"
    content_type = "application/json"
