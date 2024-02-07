from __future__ import annotations

from typing import ClassVar

from django import forms
from django.utils.translation import pgettext_lazy
from typing_extensions import TypeVar

from ..core.models import MarkdownContentModel
from . import models

TMarkdownContentModel = TypeVar(
    "TMarkdownContentModel", bound=MarkdownContentModel
)


class MarkdownContentModelForm(forms.ModelForm[TMarkdownContentModel]):
    class Meta:
        labels: ClassVar[dict[str, str]] = {"content": ""}
        widgets: ClassVar[dict[str, forms.Textarea]] = {
            "content": forms.Textarea({"rows": 2})
        }

    def clean_content(self) -> str:
        old_content = self.instance.content
        new_content: str = self.cleaned_data["content"]
        self.content_has_changed = old_content != new_content
        return new_content


class PostForm(MarkdownContentModelForm[models.Post]):
    class Meta(MarkdownContentModelForm.Meta):
        model = models.Post
        fields = ("content", "allow_commenting")


class CommentForm(MarkdownContentModelForm[models.Comment]):
    class Meta(MarkdownContentModelForm.Meta):
        model = models.Comment
        fields = ("content",)


class PostSearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.Textarea({
            "class": "form-control",
            "placeholder": pgettext_lazy("noun", "Search posts"),
            "rows": 2,
        }),
        label="",
    )
