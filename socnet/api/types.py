from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Literal, TypeAlias

    from rest_framework.request import Request

    from ..users.models import User

    SerializerFields: TypeAlias = Sequence[str] | Literal["__all__"] | None
    SerializerExclude: TypeAlias = Sequence[str] | None

    class AuthedRequest(Request):
        user: User
