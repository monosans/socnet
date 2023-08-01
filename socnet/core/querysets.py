from __future__ import annotations

from django.db.models import QuerySet
from django.db.models.functions import Extract
from typing_extensions import Self


class TimestampedModelQuerySet(QuerySet):  # type: ignore[type-arg]
    def annotate_epoch_dates(self) -> Self:
        return self.annotate(
            date_created_epoch=Extract("date_created", "epoch"),
            date_updated_epoch=Extract("date_updated", "epoch"),
        )
