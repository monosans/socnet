from __future__ import annotations

from typing import Type

from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import User as UserType

User: Type[UserType] = get_user_model()


class UserAdminChangeForm(auth_forms.UserChangeForm[UserType]):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(auth_forms.UserCreationForm[UserType]):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = User


class UserChangeForm(auth_forms.UserChangeForm[UserType]):
    password = None  # type: ignore[assignment]

    class Meta(auth_forms.UserChangeForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "image",
            "birth_date",
            "location",
            "about",
        )
        widgets = {"birth_date": forms.DateInput({"type": "date"})}


class UserSearchForm(forms.Form):
    q = forms.Field(
        widget=forms.Textarea({"rows": "2"}), label=_("Search query")
    )
    search_fields = forms.MultipleChoiceField(
        choices=(
            ("username", _("Username")),
            ("first_name", _("First name")),
            ("last_name", _("Last name")),
            ("location", _("Location")),
            ("about", _("About me")),
        ),
        widget=forms.CheckboxSelectMultiple,
        label=_("Fields to search"),
    )
