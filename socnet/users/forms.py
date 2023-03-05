from __future__ import annotations

from typing import Any

from django import forms
from django.contrib.auth import forms as auth_forms
from django.forms import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from .models import User


class InjectUserMixin:
    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        self.user = user
        super().__init__(*args, **kwargs)


class UserAdminChangeForm(auth_forms.UserChangeForm[User]):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(auth_forms.UserCreationForm[User]):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
        fields = ("email", *auth_forms.UserCreationForm.Meta.fields)


class EditProfileForm(auth_forms.UserChangeForm[User]):
    password = None  # type: ignore[assignment]

    class Meta(auth_forms.UserChangeForm.Meta):
        model = User
        fields = (
            "username",
            "display_name",
            "image",
            "birth_date",
            "location",
            "about",
        )
        widgets = {"birth_date": forms.DateInput({"type": "date"})}

    def clean_username(self) -> str:
        old_username: str = self.instance.username
        new_username: str = self.cleaned_data["username"]
        if old_username.lower() != new_username.lower():
            msg = gettext("It is only allowed to change the letters case.")
            code = "must_only_change_letters_case"
            raise ValidationError(msg, code)
        return new_username


class UserSearchForm(forms.Form):
    q = forms.Field(widget=forms.Textarea({"rows": "2"}), label=_("Search query"))
    search_fields = forms.MultipleChoiceField(
        choices=(
            ("username", _("Username")),
            ("display_name", _("Display name")),
            ("location", _("Location")),
            ("about", _("About me")),
        ),
        widget=forms.CheckboxSelectMultiple,
        label=_("Fields to search"),
    )


class AccountDeletionForm(InjectUserMixin, forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        label=_("Password"),
    )

    error_messages = {"invalid_password": _("Invalid password.")}

    def clean_password(self) -> Any:
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            msg = self.error_messages["invalid_password"]
            code = "invalid_password"
            raise forms.ValidationError(msg, code)
        return password
