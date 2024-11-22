from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Literal

    from rest_framework.request import Request

    from socnet.users.models import User

    type SerializerFields = Sequence[str] | Literal["__all__"] | None
    type SerializerExclude = Sequence[str] | None

    class AuthedRequest(Request):
        user: User
