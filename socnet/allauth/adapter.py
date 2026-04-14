from __future__ import annotations

from typing import TYPE_CHECKING, override

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.internal.userkit import user_field

if TYPE_CHECKING:
    from typing import Any

    from allauth.account.forms import BaseSignupForm
    from django.contrib.auth.base_user import AbstractBaseUser
    from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    @override
    def save_user(
        self,
        request: HttpRequest,
        user: AbstractBaseUser,
        form: BaseSignupForm,
        commit: bool = True,
    ) -> Any:
        user = super().save_user(request, user, form, commit=False)
        user_field(user, "display_name", form.cleaned_data["display_name"])
        if commit:
            user.save()
        return user
