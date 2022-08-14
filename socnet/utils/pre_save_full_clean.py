from __future__ import annotations

from functools import partial
from typing import Any

from django.db.models import Model
from django.db.models.signals import pre_save


def _full_clean(instance: Model, **kwargs: Any) -> None:
    instance.full_clean()


pre_save_full_clean = partial(pre_save.connect, _full_clean)
