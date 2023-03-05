from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _


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
