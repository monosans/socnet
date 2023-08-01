from __future__ import annotations

from functools import update_wrapper
from typing import Any, Callable, Type

from typing_extensions import ParamSpec, Protocol, TypeVar

T = TypeVar("T")
T2 = TypeVar("T2")
P = ParamSpec("P")


def process_returned_value(
    processor: Callable[[T], T2]
) -> Callable[[Callable[P, T]], Callable[P, T2]]:
    def decorator(f: Callable[P, T]) -> Callable[P, T2]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T2:
            return processor(f(*args, **kwargs))

        return update_wrapper(wrapper, f)

    return decorator


class HasPostInit(Protocol):
    def __post_init__(self) -> None:
        ...


THasPostInit = TypeVar("THasPostInit", bound=HasPostInit)


def run_post_init(cls: Type[THasPostInit]) -> Type[THasPostInit]:
    orig_init = cls.__init__

    def new_init(self: THasPostInit, *args: Any, **kwargs: Any) -> None:
        orig_init(self, *args, **kwargs)
        self.__post_init__()

    cls.__init__ = update_wrapper(  # type: ignore[method-assign]
        new_init, orig_init  # type: ignore[assignment]
    )
    return cls
