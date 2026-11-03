from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.core.cache import cache

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_django import Settings


@pytest.fixture(autouse=True)
def _media_root(settings: Settings, tmp_path: Path) -> None:
    settings.MEDIA_ROOT = str(tmp_path.resolve())


@pytest.fixture(autouse=True)
def _clear_cache() -> None:
    # allauth keeps its rate limits in the cache, which would otherwise leak between tests.
    cache.clear()
