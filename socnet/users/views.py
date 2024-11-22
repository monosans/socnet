from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import TrigramWordSimilarity
from django.db.models import Func, Value
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from socnet.core.decorators import vary_on_htmx
from socnet.core.utils import paginate
from socnet.users import forms
from socnet.users.models import User

if TYPE_CHECKING:
    from typing import Any

    from django.http import HttpResponse

    from socnet.core.types import AuthedRequest, HttpRequest


@login_required
def delete_account_view(request: AuthedRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.AccountDeletionForm(request.user, request.POST)
        if form.is_valid():
            request.user.delete()
            return redirect(settings.LOGIN_URL)
    else:
        form = forms.AccountDeletionForm(request.user)
    context = {"form": form}
    return render(request, "users/delete_account.html", context)


class AccountSecurityView(LoginRequiredMixin, TemplateView):
    template_name = "users/account_security.html"


@login_required
def edit_profile_view(request: AuthedRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.EditProfileForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect(request.user)
    else:
        form = forms.EditProfileForm(instance=request.user)
    context = {"form": form}
    return render(request, "users/edit_profile.html", context)


@vary_on_htmx
def search_users_view(request: HttpRequest) -> HttpResponse:
    users = None
    if request.GET:
        form = forms.UserSearchForm(request.GET)
        if form.is_valid():
            query: str = form.cleaned_data["q"]
            search_fields: list[str] = form.cleaned_data["search_fields"]
            expr = Func(Value(" "), *search_fields, function="CONCAT_WS")
            similarity = TrigramWordSimilarity(query, expr)
            users = (
                User.objects.only("display_name", "image", "username")
                .annotate(similarity=similarity)
                .filter(similarity__gte=0.6)
                .order_by("-similarity")
            )
    else:
        form = forms.UserSearchForm()
    context: dict[str, Any] = {
        "users": paginate(request, users, per_page=10)
        if users is not None
        else None
    }
    if request.htmx:
        template_name = "users/inc/search_users.html"
    else:
        template_name = "users/search_users.html"
        context["form"] = form
    return render(request, template_name, context)
