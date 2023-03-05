from __future__ import annotations

from django import forms

from ..core.templatetags.markdownify import MARKDOWN_HELP_TEXT
from . import models


class MessageCreationForm(forms.ModelForm[models.Message]):
    class Meta:
        model = models.Message
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                {"class": "form-control", "rows": 4, "placeholder": MARKDOWN_HELP_TEXT}
            )
        }
