from __future__ import annotations

from typing import Any, Dict

from allauth.account import forms as allauth_forms
from allauth_2fa import forms as allauth_2fa_forms
from django import forms
from django.utils.translation import gettext, gettext_lazy

from ..users.models import User

# Needed to redefine translation
gettext_lazy("Password (again)")


class LoginForm(allauth_forms.LoginForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        label = gettext("Username or email")
        self.fields["login"].label = label
        self.fields["login"].widget.attrs["placeholder"] = label


class AddEmailForm(allauth_forms.AddEmailForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].label = ""
        del self.fields["email"].widget.attrs["placeholder"]


class ResetPasswordForm(allauth_forms.ResetPasswordForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].label = ""
        del self.fields["email"].widget.attrs["placeholder"]


class SignupForm(allauth_forms.SignupForm):
    fields: Dict[str, forms.Field]

    display_name = User._meta.get_field("display_name").formfield()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        fields_order = ("display_name", "email", "username", "password1", "password2")
        self.fields = {
            field_name: self.fields[field_name] for field_name in fields_order
        }

        label = gettext("Email")
        self.fields["email"].label = label
        self.fields["email"].widget.attrs["placeholder"] = label


class TOTPDeviceForm(allauth_2fa_forms.TOTPDeviceForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["token"].label = ""
