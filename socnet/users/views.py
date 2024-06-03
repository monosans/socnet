from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import TrigramWordSimilarity
from django.db.models import Func, Value
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from . import forms
from .models import User

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from .types import AuthedRequest


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
    context = {"form": form, "users": users}
    return render(request, "users/search_users.html", context)
