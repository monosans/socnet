from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_django import Settings


@pytest.fixture(autouse=True)
def _media_root(settings: Settings, tmp_path: Path) -> None:
    settings.MEDIA_ROOT = str(tmp_path.resolve())
