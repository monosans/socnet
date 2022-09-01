from __future__ import annotations

from functools import partial
from typing import Any

from django.db.models import Model
from django.db.models.signals import pre_save


def _full_clean(instance: Model, **kwargs: Any) -> None:
    instance.full_clean(  # type: ignore[call-arg]
        validate_unique=False, validate_constraints=False
    )


pre_save_full_clean = partial(pre_save.connect, _full_clean)
