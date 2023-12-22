from __future__ import annotations

from typing import Literal

from django import template
from django.http import HttpRequest
from typing_extensions import Protocol

register = template.Library()


class Context(Protocol):
    def __getitem__(self, __key: Literal["request"]) -> HttpRequest: ...


@register.simple_tag(takes_context=True)
def query_transform(context: Context, **kwargs: str) -> str:
    params = context["request"].GET.copy()
    for k, v in kwargs.items():
        params[k] = v
    return params.urlencode()
