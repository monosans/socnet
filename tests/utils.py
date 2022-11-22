from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, Type

from django.db.models import Model


@contextmanager
def assert_count_diff(
    model: Type[Model], diff: int
) -> Generator[None, None, None]:
    enter_count = model.objects.count()
    try:
        yield
    finally:
        assert model.objects.count() == enter_count + diff
