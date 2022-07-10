from __future__ import annotations

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdminBase):
    fieldsets = (
        *(UserAdminBase.fieldsets or ()),  # make typing happy
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
    list_display = (
        "username",
        "email",
        "last_login",
        "date_joined",
        "is_staff",
    )
    readonly_fields = (
        *UserAdminBase.readonly_fields,
        "date_joined",
        "last_login",
    )
    filter_horizontal = (*UserAdminBase.filter_horizontal, "subscriptions")
