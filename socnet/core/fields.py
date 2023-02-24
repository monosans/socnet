from __future__ import annotations

from typing import Any, Optional, TypeVar

from django.db.models import CharField, Model, TextField

from . import utils

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")


class NormalizedCharField(CharField[_ST, _GT]):
    def clean(self, value: Any, model_instance: Optional[Model]) -> Any:
        return utils.normalize_str(super().clean(value, model_instance))


class NormalizedTextField(TextField[_ST, _GT]):
    def clean(self, value: Any, model_instance: Optional[Model]) -> Any:
        return utils.normalize_str(super().clean(value, model_instance))
