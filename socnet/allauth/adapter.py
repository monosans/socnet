from __future__ import annotations

from typing import TYPE_CHECKING

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field

if TYPE_CHECKING:
    from allauth.account.forms import SignupForm

    from ..core.types import HttpRequest
    from ..users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def save_user(
        self,
        request: HttpRequest,
        user: User,
        form: SignupForm,
        commit: bool = True,  # noqa: FBT001, FBT002
    ) -> User:
        user = super().save_user(request, user, form, commit=False)
        user_field(user, "display_name", form.cleaned_data["display_name"])
        if commit:
            user.save()
        return user
