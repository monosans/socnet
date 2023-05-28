from __future__ import annotations

from allauth.account.forms import SignupForm
from allauth.account.utils import user_field
from allauth_2fa.adapter import OTPAdapter
from django.http import HttpRequest

from ..users.models import User


class AuthAdapter(OTPAdapter):
    def save_user(
        self,
        request: HttpRequest,
        user: User,
        form: SignupForm,
        commit: bool = True,  # noqa: FBT001
    ) -> User:
        user = super().save_user(request, user, form, commit=False)
        user_field(user, "display_name", form.cleaned_data["display_name"])
        if commit:
            user.save()
        return user
