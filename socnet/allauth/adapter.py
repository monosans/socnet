from __future__ import annotations

from typing import TYPE_CHECKING, override

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.internal.userkit import user_field
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest

if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser
    from django.forms import BaseForm
    from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    @override
    def save_user(
        self,
        request: HttpRequest,
        user: AbstractBaseUser,
        form: BaseForm,
        commit: bool = True,
    ) -> AbstractBaseUser:
        user = super().save_user(request, user, form, commit=False)
        user_field(user, "display_name", form.cleaned_data["display_name"])
        if commit:
            user.save()
        return user
