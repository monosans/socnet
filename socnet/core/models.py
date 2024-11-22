from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from socnet.core.fields import NullAutoNowDateTimeField
from socnet.core.querysets import TimestampedModelQuerySet


class MarkdownContentModel(models.Model):
    content = models.TextField(
        verbose_name=_("content"),
        max_length=16384,
        help_text=_("Supports a safe subset of HTML and Markdown."),
    )

    class Meta(TypedModelMeta):
        abstract = True


class DateCreatedModel(models.Model):
    date_created = models.DateTimeField(
        verbose_name=_("date created"), auto_now_add=True
    )

    class Meta(TypedModelMeta):
        abstract = True


class DateUpdatedModel(models.Model):
    date_updated = NullAutoNowDateTimeField(verbose_name=_("date updated"))

    class Meta(TypedModelMeta):
        abstract = True


class TimestampedModel(DateCreatedModel, DateUpdatedModel):
    objects = TimestampedModelQuerySet.as_manager()

    class Meta(TypedModelMeta):
        abstract = True
