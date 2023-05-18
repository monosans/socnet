from __future__ import annotations

from typing import Any, Type, TypeVar

from django.db.models import CharField, Field, TextField

from socnet_rs import normalize_str

from . import decorators

TField = TypeVar("TField", bound=Field[Any, Any])


def create_normalized_str_field(field: Type[TField]) -> Type[TField]:
    return type(
        f"Normalized{field.__name__}",
        (field,),
        {"clean": decorators.process_returned_value(normalize_str)(field.clean)},
    )


NormalizedCharField = create_normalized_str_field(CharField)
NormalizedTextField = create_normalized_str_field(TextField)
