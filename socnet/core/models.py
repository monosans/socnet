from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

MARKDOWN_HELP_TEXT = _("Supports a safe subset of HTML and Markdown.")


class MarkdownContentModel(models.Model):
    content = models.TextField(
        verbose_name=_("content"), max_length=4096, help_text=MARKDOWN_HELP_TEXT
    )

    class Meta:
        abstract = True


class DateCreatedModel(models.Model):
    date_created = models.DateTimeField(
        verbose_name=_("date created"), auto_now_add=True
    )

    class Meta:
        abstract = True


class DateUpdatedModel(models.Model):
    date_updated = models.DateTimeField(verbose_name=_("date updated"), auto_now=True)

    class Meta:
        abstract = True


class TimestampedModel(DateCreatedModel, DateUpdatedModel):
    class Meta:
        abstract = True
