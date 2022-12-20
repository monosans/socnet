from __future__ import annotations

from typing import Iterator, Optional, Tuple, TypeVar, Union

from django.core.paginator import Page, Paginator
from django.db.models import Model, QuerySet
from django.http import HttpRequest

T = TypeVar("T")
# pylint: disable-next=invalid-name
TModel = TypeVar("TModel", bound=Model)


def lower_str(value: T) -> T:
    if not isinstance(value, str):
        return value
    return value.lower()  # type: ignore[return-value]


def normalize_str(value: T) -> T:
    if not isinstance(value, str):
        return value
    return "\n".join(  # type: ignore[return-value]
        " ".join(line.split())
        for line in filter(None, (line.strip() for line in value.splitlines()))
    )


def paginate(
    request: HttpRequest, object_list: QuerySet[TModel], *, per_page: int
) -> Tuple[Page[TModel], Optional[Iterator[Union[str, int]]]]:
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
    page_range = (
        posts.paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)
        if paginator.num_pages > 1
        else None
    )
    return posts, page_range
