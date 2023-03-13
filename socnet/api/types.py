from __future__ import annotations

import sys
from typing import Literal, Optional, Sequence, Union

from rest_framework.request import Request

from ..users.models import User

if sys.version_info < (3, 10):  # pragma: <3.10 cover
    from typing_extensions import TypeAlias
else:  # pragma: >=3.10 cover
    from typing import TypeAlias

SerializerFields: TypeAlias = Optional[Union[Sequence[str], Literal["__all__"]]]
SerializerExclude: TypeAlias = Optional[Sequence[str]]


class AuthedRequest(Request):
    user: User
