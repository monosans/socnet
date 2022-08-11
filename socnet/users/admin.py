from __future__ import annotations

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.utils.translation import gettext_lazy as _

from . import forms
from .models import User as UserType

User: type[UserType] = get_user_model()


@admin.register(User)
class UserAdmin(UserAdminBase):
    add_form = forms.UserAdminCreationForm
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
    filter_horizontal = (*UserAdminBase.filter_horizontal, "subscriptions")
    form = forms.UserAdminChangeForm
    list_display = (
        "username",
        "email",
        "last_login",
        "date_joined",
        "is_staff",
    )
    list_filter = (*UserAdminBase.list_filter, "date_joined", "last_login")
    readonly_fields = (
        *UserAdminBase.readonly_fields,
        "date_joined",
        "last_login",
    )
