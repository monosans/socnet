from __future__ import annotations

from typing import Any, Literal, Optional, Sequence, Type, Union

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django_filters import FilterSet
from rest_framework.serializers import ModelSerializer


def generate_filterset(serializer: Type[ModelSerializer[Any]]) -> FilterSet:
    model = serializer.Meta.model
    ignored_fields = (models.FileField, models.ForeignObjectRel, GenericForeignKey)
    serializer_fields = getattr(serializer.Meta, "fields", None)
    serializer_exclude = getattr(serializer.Meta, "exclude", None)
    fields = {
        field.attname: field.get_lookups()
        for field in (
            model._meta.get_fields()  # type: ignore[attr-defined] # noqa: SLF001
        )
        if not isinstance(field, ignored_fields)
        and _should_be_filterable(field, serializer_fields, serializer_exclude)
    }
    meta = type("Meta", (), {"model": model, "fields": fields})
    return type(f"{model.__name__}FilterSet", (FilterSet,), {"Meta": meta})


def _should_be_filterable(
    field: models.Field[Any, Any],
    fields: Optional[Union[Sequence[str], Literal["__all__"]]],
    exclude: Optional[Sequence[str]],
) -> bool:
    if fields:
        return fields == "__all__" or field.attname in fields
    if exclude:
        return field.attname not in exclude
    raise ValueError
