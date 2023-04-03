from __future__ import annotations

from typing import Any, Generator, List, Type

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django_filters import FilterSet
from rest_framework.serializers import ModelSerializer

from .types import SerializerExclude, SerializerFields

IGNORED_FIELDS = (
    models.FileField,
    models.ForeignObjectRel,
    models.ManyToManyField,
    GenericForeignKey,
)
IGNORED_LOOKUPS = frozenset(
    (
        "trigram_similar",
        "trigram_strict_word_similar",
        "trigram_word_similar",
        "unaccent",
    )
)


def generate_filterset(serializer: Type[ModelSerializer[Any]]) -> Type[FilterSet]:
    model = serializer.Meta.model
    filterable_fields = _get_filterable_fields(
        model,  # type: ignore[arg-type]
        getattr(serializer.Meta, "fields", None),
        getattr(serializer.Meta, "exclude", None),
    )
    filterset_fields = {
        field.attname: _get_lookups(field) for field in filterable_fields
    }
    meta = type("Meta", (), {"model": model, "fields": filterset_fields})
    return type(f"{model.__name__}FilterSet", (FilterSet,), {"Meta": meta})


def _get_filterable_fields(
    model: models.Model, fields: SerializerFields, exclude: SerializerExclude
) -> Generator[models.Field[Any, Any], None, None]:
    for field in model._meta.get_fields():  # noqa: SLF001
        if not isinstance(field, IGNORED_FIELDS) and _should_be_filterable(
            field, fields, exclude
        ):
            yield field


def _get_lookups(field: models.Field[Any, Any]) -> List[str]:
    return [lookup for lookup in field.get_lookups() if lookup not in IGNORED_LOOKUPS]


def _should_be_filterable(
    field: models.Field[Any, Any], fields: SerializerFields, exclude: SerializerExclude
) -> bool:
    if fields:
        return fields == "__all__" or field.attname in fields
    if exclude:
        return field.attname not in exclude
    raise ValueError
