from __future__ import annotations

from collections.abc import Iterator
from typing import no_type_check

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django_filters import FilterSet
from rest_framework.serializers import ModelSerializer
from typing_extensions import Any, Protocol, TypeVar

from .types import SerializerExclude, SerializerFields

IGNORED_FIELDS = (
    models.FileField,
    models.ForeignObjectRel,
    models.ManyToManyField,
    GenericForeignKey,
)
IGNORED_LOOKUPS = frozenset(("unaccent",))


class HasModelSerializer(Protocol):
    serializer_class: type[ModelSerializer[Any]]


THasModelSerializer = TypeVar("THasModelSerializer", bound=HasModelSerializer)


@no_type_check
def generate_filterset(view: THasModelSerializer, /) -> THasModelSerializer:
    view.filterset_class = generate_filterset_from_serializer(
        view.serializer_class
    )
    return view


def generate_filterset_from_serializer(
    serializer: type[ModelSerializer[Any]],
) -> type[FilterSet]:
    model = serializer.Meta.model
    filterable_fields = _get_filterable_fields(
        model,
        getattr(serializer.Meta, "fields", None),
        getattr(serializer.Meta, "exclude", None),
    )
    filterset_fields = {
        field.attname: _get_lookups(field) for field in filterable_fields
    }
    meta = type("Meta", (), {"model": model, "fields": filterset_fields})
    return type(f"{model.__name__}FilterSet", (FilterSet,), {"Meta": meta})


def _get_filterable_fields(
    model: type[models.Model],
    fields: SerializerFields,
    exclude: SerializerExclude,
) -> Iterator[models.Field[Any, Any]]:
    for field in model._meta.get_fields():
        if not isinstance(field, IGNORED_FIELDS) and _should_be_filterable(
            field, fields, exclude
        ):
            yield field


def _get_lookups(field: models.Field[Any, Any]) -> list[str]:
    return [
        lookup
        for lookup in field.get_lookups()
        if lookup not in IGNORED_LOOKUPS
    ]


def _should_be_filterable(
    field: models.Field[Any, Any],
    fields: SerializerFields,
    exclude: SerializerExclude,
) -> bool:
    if fields:
        return fields == "__all__" or field.attname in fields
    if exclude:
        return field.attname not in exclude
    raise ValueError  # pragma: no cover
