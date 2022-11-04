from __future__ import annotations

from copy import deepcopy

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from . import forms

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = deepcopy(BaseUserAdmin.add_fieldsets)
    add_fieldsets[0][1]["fields"] = ("email", *add_fieldsets[0][1]["fields"])

    add_form = forms.UserAdminCreationForm
    fieldsets = (
        *(BaseUserAdmin.fieldsets or ()),
        (
            _("Other"),
            {
                "fields": (
                    "birth_date",
                    "location",
                    "image",
                    "about",
                    "subscriptions",
                )
            },
        ),
    )
    filter_horizontal = (*BaseUserAdmin.filter_horizontal, "subscriptions")
    form = forms.UserAdminChangeForm
    list_display = (
        "username",
        "email",
        "last_login",
        "date_joined",
        "is_staff",
    )
    list_filter = (*BaseUserAdmin.list_filter, "date_joined", "last_login")
    readonly_fields = (
        *BaseUserAdmin.readonly_fields,
        "date_joined",
        "last_login",
    )
