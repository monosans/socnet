from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class PostForm(forms.ModelForm[models.Post]):
    class Meta:
        model = models.Post
        fields = ("content",)
        labels = {"content": ""}


class CommentForm(forms.ModelForm[models.Comment]):
    class Meta:
        model = models.Comment
        fields = ("content",)
        labels = {"content": ""}


class PostSearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.Textarea(
            {"class": "form-control", "placeholder": _("Search posts")}
        ),
        label="",
    )
