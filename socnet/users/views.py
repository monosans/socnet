from __future__ import annotations

from typing import List, Optional, Type

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchRank, SearchVector
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from . import forms
from .models import User as UserType
from .types import AuthedRequest

User: Type[UserType] = get_user_model()


@login_required
@require_http_methods(["GET", "POST"])
def edit_profile(request: AuthedRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.UserChangeForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
    else:
        form = forms.UserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, "users/edit_profile.html", context)


@require_http_methods(["GET"])
def users_search_view(request: HttpRequest) -> HttpResponse:
    users: Optional[QuerySet[UserType]] = None
    if request.GET:
        form = forms.UsersSearchForm(request.GET)
        if form.is_valid():
            query: str = form.cleaned_data["q"]
            search_fields: List[str] = form.cleaned_data["search_fields"]
            rank = SearchRank(vector=SearchVector(*search_fields), query=query)
            users = (
                User.objects.annotate(rank=rank)
                .filter(rank__gt=0)
                .order_by("-rank", "username")
                .only("username", "first_name", "last_name", "image")
            )
    else:
        form = forms.UsersSearchForm()
    context = {"form": form, "users": users}
    return render(request, "users/users_search.html", context)
