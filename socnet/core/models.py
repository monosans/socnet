from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from .fields import NullAutoNowDateTimeField
from .querysets import TimestampedModelQuerySet


class MarkdownContentModel(models.Model):
    content = models.TextField(
        verbose_name=_("content"),
        max_length=16384,
        help_text=_("Supports a safe subset of HTML and Markdown."),
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
    date_updated = NullAutoNowDateTimeField(verbose_name=_("date updated"))

    class Meta:
        abstract = True


class TimestampedModel(DateCreatedModel, DateUpdatedModel):
    objects = TimestampedModelQuerySet.as_manager()

    class Meta:
        abstract = True
