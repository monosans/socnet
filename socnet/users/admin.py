from __future__ import annotations

from typing import Type

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import forms
from .models import User as UserType

User: Type[UserType] = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = forms.UserAdminCreationForm
    fieldsets = (
        *(BaseUserAdmin.fieldsets or ()),  # make typing happy
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
