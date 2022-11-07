from __future__ import annotations

from typing import List

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchRank, SearchVector
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_safe

from . import forms
from .models import User
from .types import AuthedRequest


@require_http_methods(["GET", "HEAD", "POST"])
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


@require_http_methods(["GET", "HEAD", "POST"])
@login_required
def edit_profile_view(request: AuthedRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.EditProfileForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
    else:
        form = forms.EditProfileForm(instance=request.user)
    context = {"form": form}
    return render(request, "users/edit_profile.html", context)


@require_safe
def search_users_view(request: HttpRequest) -> HttpResponse:
    users = None
    if request.GET:
        form = forms.UserSearchForm(request.GET)
        if form.is_valid():
            query: str = form.cleaned_data["q"]
            search_fields: List[str] = form.cleaned_data["search_fields"]
            rank = SearchRank(vector=SearchVector(*search_fields), query=query)
            users = (
                User.objects.annotate(rank=rank)
                .filter(rank__gt=0)
                .order_by("-rank", "username")
                .only("display_name", "image", "username")
            )
    else:
        form = forms.UserSearchForm()
    context = {"form": form, "users": users}
    return render(request, "users/search_users.html", context)
