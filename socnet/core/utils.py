from __future__ import annotations

import time
from typing import TYPE_CHECKING

from django.core.paginator import Paginator
from typing_extensions import overload

if TYPE_CHECKING:
    import datetime
    from collections.abc import Iterator
    from typing import Literal

    from django.core.paginator import Page
    from django.db.models import Model, QuerySet
    from typing_extensions import TypeVar

    from ..core.types import HttpRequest

    TModel = TypeVar("TModel", bound=Model)


def dt_to_epoch(dt: datetime.date) -> int:
    return int(time.mktime(dt.timetuple()))


@overload
def paginate(
    request: HttpRequest,
    object_list: QuerySet[TModel],
    *,
    per_page: int,
    include_page_range: Literal[True],
) -> tuple[Page[TModel], Iterator[str | int] | None]: ...


@overload
def paginate(
    request: HttpRequest,
    object_list: QuerySet[TModel],
    *,
    per_page: int,
    include_page_range: Literal[False],
) -> Page[TModel]: ...


def paginate(
    request: HttpRequest,
    object_list: QuerySet[TModel],
    *,
    per_page: int,
    include_page_range: bool,
) -> tuple[Page[TModel], Iterator[str | int] | None] | Page[TModel]:
    paginator = Paginator(object_list, per_page=per_page)
    try:
        page = int(request.GET["page"])
    except (KeyError, ValueError):
        page = 1
    else:
        if page < 1:
            page = 1
        elif page > paginator.num_pages:
            # If the user sets a page number greater than the
            # last page number, show him the last page.
            page = paginator.num_pages
    posts = paginator.page(page)
    if not include_page_range:
        return posts

    page_range = (
        posts.paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)
        if paginator.num_pages > 1
        else None
    )
    return posts, page_range
