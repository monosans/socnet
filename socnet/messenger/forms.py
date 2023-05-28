from __future__ import annotations

from django import forms

from . import models


class MessageCreationForm(forms.ModelForm[models.Message]):
    class Meta:
        model = models.Message
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                {
                    "class": "form-control border-0 rounded-top-0",
                    "placeholder": models.Message._meta.get_field(  # noqa: SLF001
                        "content"
                    ).help_text,
                    "rows": 2,
                }
            )
        }
