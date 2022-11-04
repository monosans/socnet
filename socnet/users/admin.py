from __future__ import annotations

from copy import deepcopy
from typing import Iterable, Tuple, TypeVar

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from . import forms

T = TypeVar("T")

User = get_user_model()


def filter_fields(fields: Iterable[T]) -> Tuple[T, ...]:
    deleted_fields = {"date_joined", "first_name", "last_login", "last_name"}
    return tuple(field for field in fields if field not in deleted_fields)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = deepcopy(BaseUserAdmin.add_fieldsets)
    add_fieldsets[0][1]["fields"] = ("email", *add_fieldsets[0][1]["fields"])

    add_form = forms.UserAdminCreationForm

    fieldsets = []
    for name, field_options in BaseUserAdmin.fieldsets or ():
        filtered_field_options = {
            k: (
                filter_fields(v)
                if k == "fields" and isinstance(v, Iterable)
                else v
            )
            for k, v in field_options.items()
        }
        if filtered_field_options["fields"]:
            fieldsets.append((name, filtered_field_options))
    fieldsets.append(
        (
            _("Other"),
            {
                "fields": (
                    "display_name",
                    "birth_date",
                    "location",
                    "image",
                    "about",
                    "subscriptions",
                )
            },
        )
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
