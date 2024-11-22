from __future__ import annotations

from typing import TYPE_CHECKING

from django import forms
from django.utils.translation import pgettext_lazy

from socnet.messenger import models

if TYPE_CHECKING:
    from typing import ClassVar


class MessageCreationForm(forms.ModelForm[models.Message]):
    class Meta:
        model = models.Message
        fields = ("content",)
        widgets: ClassVar[dict[str, forms.Textarea]] = {
            "content": forms.Textarea({
                "class": "form-control border-0 rounded-top-0",
                "placeholder": models.Message._meta.get_field(
                    "content"
                ).help_text,
                "rows": 2,
            })
        }


class MessageSearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.Textarea({
            "class": "form-control border-0 rounded-bottom-0",
            "placeholder": pgettext_lazy("noun", "Search messages"),
            "rows": 2,
        }),
        label="",
    )
