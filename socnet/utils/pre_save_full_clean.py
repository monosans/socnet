from __future__ import annotations

from typing import Any, Type, TypeVar

from django.db.models import Model
from django.db.models.signals import pre_save

TModel = TypeVar("TModel", bound=Model)


def pre_save_full_clean(model: Type[TModel]) -> None:
    def full_clean(instance: TModel, **kwargs: Any) -> None:
        instance.full_clean()

    pre_save.connect(full_clean, model)
