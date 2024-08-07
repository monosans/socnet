from __future__ import annotations

from typing import TYPE_CHECKING

from django import template

if TYPE_CHECKING:
    from typing import Literal

    from django.http import HttpRequest
    from typing_extensions import Protocol

    class Context(Protocol):
        def __getitem__(self, _: Literal["request"], /) -> HttpRequest: ...


register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context: Context, **kwargs: str) -> str:
    params = context["request"].GET.copy()
    for k, v in kwargs.items():
        params[k] = v
    return params.urlencode()
