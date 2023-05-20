from __future__ import annotations

from typing import Any

from allauth.account import forms as allauth_forms
from allauth_2fa import forms as allauth_2fa_forms
from django.utils.translation import gettext, gettext_lazy as _, pgettext_lazy

# Needed to redefine translation
pgettext_lazy("field label", "Login")
_("Password (again)")


class LoginForm(allauth_forms.LoginForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["login"].widget.attrs["placeholder"] = self.fields["login"].label


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
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        label = gettext("Email")
        self.fields["email"].label = label
        self.fields["email"].widget.attrs["placeholder"] = label


class TOTPDeviceForm(allauth_2fa_forms.TOTPDeviceForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["token"].label = ""
