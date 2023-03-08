from __future__ import annotations

from django import forms

from ..core.models import MARKDOWN_HELP_TEXT
from . import models


class MessageCreationForm(forms.ModelForm[models.Message]):
    class Meta:
        model = models.Message
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                {"class": "form-control", "placeholder": MARKDOWN_HELP_TEXT}
            )
        }
