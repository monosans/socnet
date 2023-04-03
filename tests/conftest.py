from __future__ import annotations

from pathlib import Path
from typing import List

import pytest
from django.conf import LazySettings


def pytest_collection_modifyitems(items: List[pytest.Item]) -> None:
    for item in items:
        item.add_marker("django_db")


@pytest.fixture(autouse=True)
def _media_root(settings: LazySettings, tmp_path: Path) -> None:
    settings.MEDIA_ROOT = str(tmp_path.resolve())
