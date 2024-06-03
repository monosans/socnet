from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal, TypeAlias

from rest_framework.request import Request

if TYPE_CHECKING:
    from ..users.models import User

SerializerFields: TypeAlias = Sequence[str] | Literal["__all__"] | None
SerializerExclude: TypeAlias = Sequence[str] | None


class AuthedRequest(Request):
    user: User
