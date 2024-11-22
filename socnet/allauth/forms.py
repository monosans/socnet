from __future__ import annotations

from typing import TYPE_CHECKING

from allauth.account import forms as allauth_forms
from django.utils.translation import gettext, gettext_lazy

from socnet.users.models import User

if TYPE_CHECKING:
    from typing import Any

    from django import forms

# Needed to redefine translation
gettext_lazy("Email")
gettext_lazy("Password (again)")


class AddEmailForm(allauth_forms.AddEmailForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].label = ""
        del self.fields["email"].widget.attrs["placeholder"]


class LoginForm(allauth_forms.LoginForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["password"].help_text = ""
        label = gettext("Username or email")
        self.fields["login"].label = label
        self.fields["login"].widget.attrs["placeholder"] = label


class ResetPasswordForm(allauth_forms.ResetPasswordForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].label = ""
        del self.fields["email"].widget.attrs["placeholder"]


class SignupForm(allauth_forms.SignupForm):
    fields: dict[str, forms.Field]

    display_name = User._meta.get_field("display_name").formfield()
    field_order = (
        "display_name",
        "email",
        "username",
        "password1",
        "password2",
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = self.fields[
            "email"
        ].label
