from django.http import HttpRequest

from .models import User as UserType


class AuthedRequest(HttpRequest):
    user: UserType
