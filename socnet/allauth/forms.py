from __future__ import annotations

from typing import Dict

from allauth.account import forms as allauth_forms
from allauth_2fa import forms as allauth_2fa_forms
from django import forms
from django.utils.translation import gettext, gettext_lazy

from ..core.decorators import run_post_init
from ..users.models import User

# Needed to redefine translation
gettext_lazy("Password (again)")


@run_post_init
class AddEmailForm(allauth_forms.AddEmailForm):
    def __post_init__(self) -> None:
        self.fields["email"].label = ""
        del self.fields["email"].widget.attrs["placeholder"]


@run_post_init
class LoginForm(allauth_forms.LoginForm):
    def __post_init__(self) -> None:
        label = gettext("Username or email")
        self.fields["login"].label = label
        self.fields["login"].widget.attrs["placeholder"] = label


@run_post_init
class ResetPasswordForm(allauth_forms.ResetPasswordForm):
    def __post_init__(self) -> None:
        self.fields["email"].label = ""
        del self.fields["email"].widget.attrs["placeholder"]


@run_post_init
class SignupForm(allauth_forms.SignupForm):
    fields: Dict[str, forms.Field]

    display_name = User._meta.get_field("display_name").formfield()
    field_order = (
        "display_name",
        "email",
        "username",
        "password1",
        "password2",
    )

    def __post_init__(self) -> None:
        label = gettext("Email")
        self.fields["email"].label = label
        self.fields["email"].widget.attrs["placeholder"] = label


@run_post_init
class TOTPDeviceForm(allauth_2fa_forms.TOTPDeviceForm):
    def __post_init__(self) -> None:
        self.fields["otp_token"].label = ""
