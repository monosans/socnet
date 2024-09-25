from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import QuerySet
from django.db.models.functions import Extract

if TYPE_CHECKING:
    from django.db.models import Model
    from django_stubs_ext import WithAnnotations
    from typing_extensions import TypedDict, TypeVar

    _TModel = TypeVar("_TModel", bound=Model, covariant=True)  # noqa: PLC0105

    class EpochDates(TypedDict):
        date_created_epoch: int
        date_updated_epoch: int


class TimestampedModelQuerySet(QuerySet["_TModel"]):
    def annotate_epoch_dates(
        self,
    ) -> TimestampedModelQuerySet[WithAnnotations[_TModel, EpochDates]]:
        return self.annotate(  # type: ignore[no-any-return]
            date_created_epoch=Extract("date_created", "epoch"),
            date_updated_epoch=Extract("date_updated", "epoch"),
        )
