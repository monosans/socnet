from __future__ import annotations

from rest_framework.request import Request

from ..users.models import User as UserType


# pylint: disable-next=abstract-method
class AuthedRequest(Request):
    user: UserType
