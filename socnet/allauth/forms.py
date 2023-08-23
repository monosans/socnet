from __future__ import annotations

from typing import Dict

from allauth.account import forms as allauth_forms
from allauth_2fa import forms as allauth_2fa_forms
from django import forms
from django.utils.translation import gettext, gettext_lazy
from typing_extensions import Any

from ..users.models import User

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
        label = gettext("Username or email")
        self.fields["login"].label = label
        self.fields["login"].widget.attrs["placeholder"] = label


class ResetPasswordForm(allauth_forms.ResetPasswordForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].label = ""
        del self.fields["email"].widget.attrs["placeholder"]


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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = self.fields[
            "email"
        ].label


class TOTPDeviceForm(allauth_2fa_forms.TOTPDeviceForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["otp_token"].label = ""
