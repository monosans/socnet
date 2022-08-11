from __future__ import annotations

from django import forms

from . import models


class MessageCreationForm(forms.ModelForm[models.Message]):
    class Meta:
        model = models.Message
        fields = ("text",)
        widgets = {
            "text": forms.Textarea({"class": "form-control", "rows": 4})
        }
