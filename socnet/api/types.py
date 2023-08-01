from __future__ import annotations

from typing import Literal, Optional, Sequence, Union

from rest_framework.request import Request
from typing_extensions import TypeAlias

from ..users.models import User

SerializerFields: TypeAlias = Optional[Union[Sequence[str], Literal["__all__"]]]
SerializerExclude: TypeAlias = Optional[Sequence[str]]


class AuthedRequest(Request):
    user: User
