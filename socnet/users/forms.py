from __future__ import annotations

from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _

from .models import User


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
        fields = ("display_name", "image", "birth_date", "location", "about")
        widgets = {"birth_date": forms.DateInput({"type": "date"})}


class UserSearchForm(forms.Form):
    q = forms.Field(
        widget=forms.Textarea({"rows": "2"}), label=_("Search query")
    )
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
