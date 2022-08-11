from __future__ import annotations

from typing import Any, TypeVar

from django.db.models import Model
from django.db.models.signals import pre_save

TModel = TypeVar("TModel", bound=Model)


def pre_save_full_clean(model: type[TModel]) -> None:
    def full_clean(instance: TModel, **kwargs: Any) -> None:
        instance.full_clean()

    pre_save.connect(full_clean, model)
