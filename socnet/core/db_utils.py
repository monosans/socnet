from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models.functions import Extract

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django_stubs_ext import WithAnnotations
    from typing_extensions import TypedDict

    from socnet.core.models import TimestampedModel

    class EpochDates(TypedDict):
        date_created_epoch: int
        date_updated_epoch: int


def annotate_epoch_dates[T: TimestampedModel](
    qs: QuerySet[T],
) -> QuerySet[WithAnnotations[T, EpochDates]]:
    return qs.annotate(  # type: ignore[no-any-return]
        date_created_epoch=Extract("date_created", "epoch"),
        date_updated_epoch=Extract("date_updated", "epoch"),
    )
