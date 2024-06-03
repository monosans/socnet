from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from django import template
from typing_extensions import Protocol

if TYPE_CHECKING:
    from django.http import HttpRequest

register = template.Library()


class Context(Protocol):
    def __getitem__(self, _: Literal["request"], /) -> HttpRequest: ...


@register.simple_tag(takes_context=True)
def query_transform(context: Context, **kwargs: str) -> str:
    params = context["request"].GET.copy()
    for k, v in kwargs.items():
        params[k] = v
    return params.urlencode()
