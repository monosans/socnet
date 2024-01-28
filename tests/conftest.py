from __future__ import annotations

from pathlib import Path

import pytest
from django.conf import LazySettings


@pytest.fixture(autouse=True)
def _media_root(settings: LazySettings, tmp_path: Path) -> None:
    settings.MEDIA_ROOT = str(tmp_path.resolve())
