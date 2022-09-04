from __future__ import annotations

from typing import Any

from django.apps import apps
from django.db.models import Model
from django.db.models.signals import pre_save


def full_clean(instance: Model, **kwargs: Any) -> None:
    instance.full_clean(  # type: ignore[call-arg]
        validate_unique=False, validate_constraints=False
    )


for model in apps.get_models(include_auto_created=True):
    pre_save.connect(full_clean, sender=model)
