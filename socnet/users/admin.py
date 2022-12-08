from __future__ import annotations

from copy import deepcopy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import forms
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = deepcopy(BaseUserAdmin.add_fieldsets)
    add_fieldsets[0][1]["fields"] = ("email", *add_fieldsets[0][1]["fields"])
    add_form = forms.UserAdminCreationForm
    fieldsets = (
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
    filter_horizontal = (*BaseUserAdmin.filter_horizontal, "subscriptions")
    form = forms.UserAdminChangeForm
    list_display = ("id", "username", "email", "display_name", "is_staff")
    search_fields = ("username", "display_name", "email")
