from __future__ import annotations

from typing import Any, Optional, Union

from django.contrib.postgres.fields import CIEmailField
from django.db.models import CharField, Model, TextField
from django.db.models.expressions import Combinable

from . import utils


class LowercaseCharField(CharField[Union[str, int, Combinable], str]):
    def clean(self, value: Any, model_instance: Optional[Model]) -> Any:
        return utils.lower_str(super().clean(value, model_instance))


class LowercaseEmailField(CIEmailField):
    def clean(self, value: Any, model_instance: Optional[Model]) -> Any:
        return utils.lower_str(super().clean(value, model_instance))


class NormalizedCharField(CharField[Union[str, int, Combinable], str]):
    def clean(self, value: Any, model_instance: Optional[Model]) -> Any:
        return utils.normalize_str(super().clean(value, model_instance))


class NormalizedTextField(TextField[Union[str, Combinable], str]):
    def clean(self, value: Any, model_instance: Optional[Model]) -> Any:
        return utils.normalize_str(super().clean(value, model_instance))
