from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import QuerySet
from django.db.models.functions import Extract

if TYPE_CHECKING:
    from typing import TypedDict

    from django_stubs_ext import WithAnnotations

    from socnet.core.models import TimestampedModel

    class EpochDates(TypedDict):
        date_created_epoch: int
        date_updated_epoch: int


class TimestampedModelQuerySet[T: TimestampedModel](QuerySet[T]):
    def annotate_epoch_dates(
        self,
    ) -> TimestampedModelQuerySet[WithAnnotations[T, EpochDates]]:
        return self.annotate(  # type: ignore[no-any-return]
            date_created_epoch=Extract("date_created", "epoch"),
            date_updated_epoch=Extract("date_updated", "epoch"),
        )
