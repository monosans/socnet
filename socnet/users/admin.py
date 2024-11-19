from __future__ import annotations

from copy import deepcopy

from allauth.account.decorators import secure_admin_login
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import forms
from .models import User

# https://docs.allauth.org/en/latest/common/admin.html#admin
admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(BaseUserAdmin[User]):
    add_fieldsets = deepcopy(BaseUserAdmin.add_fieldsets)
    add_fieldsets[0][1]["fields"] = (
        "display_name",
        "email",
        "username",
        "password1",
        "password2",
    )
    add_form = forms.UserAdminCreationForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "display_name",
                    "image",
                    "birth_date",
                    "location",
                    "about",
                    "show_last_login",
                    "date_joined",
                    "last_login",
                    "subscriptions",
                )
            },
        ),
        BaseUserAdmin.fieldsets[2],  # type: ignore[index]
    )
    filter_horizontal = (*BaseUserAdmin.filter_horizontal, "subscriptions")
    form = forms.UserAdminChangeForm
    list_display = ("id", "username", "email", "display_name", "is_staff")
    list_filter = (*BaseUserAdmin.list_filter, "date_joined", "last_login")
    readonly_fields = ("date_joined", "last_login")
    search_fields = ("@username", "@display_name", "@email")
