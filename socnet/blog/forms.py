from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class PostForm(forms.ModelForm[models.Post]):
    class Meta:
        model = models.Post
        fields = ("content",)


class PostCommentForm(forms.ModelForm[models.PostComment]):
    class Meta:
        model = models.PostComment
        fields = ("content",)


class PostSearchForm(forms.Form):
    q = forms.Field(
        widget=forms.Textarea(
            {"class": "form-control", "placeholder": _("Search posts")}
        ),
        label=_("Search query"),
    )
