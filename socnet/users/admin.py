from __future__ import annotations

from copy import deepcopy
from typing import Iterable, Tuple, TypeVar

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import forms
from .models import User

T = TypeVar("T")


def filter_fields(fields: Iterable[T]) -> Tuple[T, ...]:
    deleted_fields = {"date_joined", "first_name", "last_login", "last_name"}
    return tuple(field for field in fields if field not in deleted_fields)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = deepcopy(BaseUserAdmin.add_fieldsets)
    add_fieldsets[0][1]["fields"] = ("email", *add_fieldsets[0][1]["fields"])

    add_form = forms.UserAdminCreationForm
    fieldsets = (  # type: ignore[assignment]
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "display_name",
                    "birth_date",
                    "image",
                    "location",
                    "about",
                )
            },
        ),
        (_("Blog"), {"fields": ("subscriptions",)}),
        BaseUserAdmin.fieldsets[2],  # type: ignore[index]
    )
    filter_horizontal = (
        *filter_fields(BaseUserAdmin.filter_horizontal),
        "subscriptions",
    )
    form = forms.UserAdminChangeForm
    list_display = filter_fields(BaseUserAdmin.list_display)
    list_filter = filter_fields(BaseUserAdmin.list_filter)
    readonly_fields = filter_fields(BaseUserAdmin.readonly_fields)
    search_fields = filter_fields(BaseUserAdmin.search_fields)
