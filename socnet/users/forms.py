from __future__ import annotations

from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext, gettext_lazy as _

from .models import User

if TYPE_CHECKING:
    from typing import Any, ClassVar

    from django_stubs_ext import StrPromise


class InjectUserMixin:
    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        self.user = user
        super().__init__(*args, **kwargs)


class UserAdminChangeForm(auth_forms.UserChangeForm[User]):
    class Meta(auth_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User


class UserAdminCreationForm(auth_forms.BaseUserCreationForm[User]):
    class Meta(auth_forms.BaseUserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("display_name", "email", "username")


class EditProfileForm(auth_forms.UserChangeForm[User]):
    password = None  # type: ignore[assignment]

    class Meta(auth_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = (
            "display_name",
            "username",
            "image",
            "birth_date",
            "location",
            "about",
            "show_last_login",
        )
        widgets: ClassVar[dict[str, forms.Textarea]] = {
            "about": forms.Textarea({"rows": 1})
        }

    def clean_username(self) -> str:
        old_username = self.instance.username
        new_username: str = self.cleaned_data["username"]
        if old_username.casefold() != new_username.casefold():
            msg = gettext("It is only allowed to change the letters case.")
            code = "must_only_change_letters_case"
            raise forms.ValidationError(msg, code)
        return new_username


class UserSearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.Textarea({"rows": 1}), label=_("Search query")
    )
    search_fields = forms.MultipleChoiceField(
        choices=(
            ("display_name", _("Display name")),
            ("username", _("Username")),
            ("location", _("Location")),
            ("about", _("About me")),
        ),
        widget=forms.CheckboxSelectMultiple,
        label=_("Fields to search"),
    )


class AccountDeletionForm(InjectUserMixin, forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput({"autocomplete": "current-password"}),
        label=_("Password"),
    )

    error_messages: ClassVar[dict[str, StrPromise]] = {
        "invalid_password": _("Invalid password.")
    }

    def clean_password(self) -> str:
        password: str = self.cleaned_data["password"]
        if not self.user.check_password(password):
            msg = self.error_messages["invalid_password"]
            code = "invalid_password"
            raise forms.ValidationError(msg, code)
        return password
