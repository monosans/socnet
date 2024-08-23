from __future__ import annotations

import time
from typing import TYPE_CHECKING

from django.core.paginator import Paginator

if TYPE_CHECKING:
    import datetime

    from django.core.paginator import Page
    from django.db.models import Model, QuerySet
    from typing_extensions import TypeVar

    from ..core.types import HttpRequest

    TModel = TypeVar("TModel", bound=Model)


def dt_to_epoch(dt: datetime.date) -> int:
    return int(time.mktime(dt.timetuple()))


def paginate(
    request: HttpRequest, object_list: QuerySet[TModel], *, per_page: int
) -> Page[TModel]:
    return Paginator(object_list, per_page=per_page).get_page(
        request.GET.get("page", 1)
    )
