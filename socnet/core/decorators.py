from __future__ import annotations

import functools
from typing import TYPE_CHECKING

from django.core.exceptions import BadRequest
from django.views.decorators.vary import vary_on_headers

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

    from .types import HttpRequest


def copy_type_hints[**P, T](
    _f: Callable[P, Any], /
) -> Callable[[Callable[..., T]], Callable[P, T]]:
    def wrapper(func: Callable[..., T]) -> Callable[P, T]:
        return func

    return wrapper


def process_returned_value[**P, T, T2](
    processor: Callable[[T], T2],
) -> Callable[[Callable[P, T]], Callable[P, T2]]:
    def decorator(f: Callable[P, T]) -> Callable[P, T2]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T2:
            return processor(f(*args, **kwargs))

        return functools.update_wrapper(wrapper, f)

    return decorator


def require_htmx[**P, T](f: Callable[P, T], /) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        if TYPE_CHECKING:
            assert isinstance(args[0], HttpRequest)
        if not args[0].htmx:
            raise BadRequest
        return f(*args, **kwargs)

    return functools.update_wrapper(wrapper, f)


vary_on_htmx = vary_on_headers("HX-Request")
