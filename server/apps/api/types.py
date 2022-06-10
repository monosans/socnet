from rest_framework.request import Request

from ..users.models import User as UserType


class AuthedRequest(Request):
    user: UserType
