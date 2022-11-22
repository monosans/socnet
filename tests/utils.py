from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

from django.db.models import Model


class AssertCountDiff:
    __slots__ = ("model", "diff", "enter_count")

    def __init__(self, model: Type[Model], diff: int) -> None:
        self.model = model
        self.diff = diff

    def _get_count(self) -> int:
        return self.model.objects.count()

    def __enter__(self) -> None:
        self.enter_count = self._get_count()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        assert self._get_count() == self.enter_count + self.diff
