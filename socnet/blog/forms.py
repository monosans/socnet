from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class PostCreationForm(forms.ModelForm[models.Post]):
    class Meta:
        model = models.Post
        fields = ("text", "image")


class PostCommentCreationForm(forms.ModelForm[models.PostComment]):
    class Meta:
        model = models.PostComment
        fields = ("text", "image")


class PostSearchForm(forms.Form):
    q = forms.Field(
        widget=forms.Textarea(
            {"rows": "1", "class": "form-control", "placeholder": _("Search posts")}
        ),
        label=_("Search query"),
    )
