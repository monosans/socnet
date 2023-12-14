from __future__ import annotations

import functools
from typing import Callable

from typing_extensions import Any, ParamSpec, TypeVar

T = TypeVar("T")
T2 = TypeVar("T2")
P = ParamSpec("P")


def copy_type_hints(
    _f: Callable[P, Any], /
) -> Callable[[Callable[..., T]], Callable[P, T]]:
    def wrapper(func: Callable[..., T]) -> Callable[P, T]:
        return func

    return wrapper


def process_returned_value(
    processor: Callable[[T], T2],
) -> Callable[[Callable[P, T]], Callable[P, T2]]:
    def decorator(f: Callable[P, T]) -> Callable[P, T2]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T2:
            return processor(f(*args, **kwargs))

        return functools.update_wrapper(wrapper, f)

    return decorator
