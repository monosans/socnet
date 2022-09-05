from __future__ import annotations

from typing import Any, Optional, Union

from django.db.models import CharField, Model, TextField
from django.db.models.expressions import Combinable

from . import utils


class LowercaseCharField(CharField[Union[str, int, Combinable], str]):
    def clean(self, value: Any, model_instance: Optional[Model]) -> Any:
        result = super().clean(value, model_instance)
        if not isinstance(result, str):
            return result
        return result.lower()


class NormalizedCharField(CharField[Union[str, int, Combinable], str]):
    def clean(self, value: Any, model_instance: Optional[Model]) -> Any:
        return utils.normalize_str(super().clean(value, model_instance))


class NormalizedTextField(TextField[Union[str, Combinable], str]):
    def clean(self, value: Any, model_instance: Optional[Model]) -> Any:
        return utils.normalize_str(super().clean(value, model_instance))
