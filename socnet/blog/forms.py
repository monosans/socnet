from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

from ..core.templatetags.markdownify import MARKDOWN_HELP_TEXT
from . import models


class PostCreationForm(forms.ModelForm[models.Post]):
    class Meta:
        model = models.Post
        fields = ("content",)
        help_texts = {"content": MARKDOWN_HELP_TEXT}


class PostCommentCreationForm(forms.ModelForm[models.PostComment]):
    class Meta:
        model = models.PostComment
        fields = ("content",)
        help_texts = {"content": MARKDOWN_HELP_TEXT}


class PostSearchForm(forms.Form):
    q = forms.Field(
        widget=forms.Textarea(
            {"class": "form-control", "placeholder": _("Search posts")}
        ),
        label=_("Search query"),
    )
