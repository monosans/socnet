from __future__ import annotations

from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ..users.models import User as UserType
from . import models

User: type[UserType] = get_user_model()


class PostsSearchForm(forms.Form):
    search_query = forms.Field(
        widget=forms.Textarea(
            {
                "rows": "1",
                "class": "form-control",
                "placeholder": _("Search posts"),
            }
        ),
        label=_("Search query"),
    )


class UsersSearchForm(forms.Form):
    search_query = forms.Field(
        widget=forms.Textarea({"rows": "2"}), label=_("Search query")
    )
    fields_to_search = forms.MultipleChoiceField(
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


class PostCommentCreationForm(forms.ModelForm[models.PostComment]):
    class Meta:
        model = models.PostComment
        fields = ("text", "image")


class PostCreationForm(forms.ModelForm[models.Post]):
    class Meta:
        model = models.Post
        fields = ("text", "image")


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
