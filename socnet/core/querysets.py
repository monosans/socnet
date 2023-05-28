from __future__ import annotations

import sys
from typing import Optional, TypedDict

from django.db.models import QuerySet
from django.db.models.functions import Extract

if sys.version_info < (3, 11):  # pragma: <3.11 cover
    from typing_extensions import Self
else:  # pragma: >=3.11 cover
    from typing import Self


class EpochDates(TypedDict):
    date_created_epoch: int
    date_updated_epoch: Optional[int]


class TimestampedModelQuerySet(QuerySet):  # type: ignore[type-arg]
    def annotate_epoch_dates(self) -> Self:
        return self.annotate(
            date_created_epoch=Extract("date_created", "epoch"),
            date_updated_epoch=Extract("date_updated", "epoch"),
        )
