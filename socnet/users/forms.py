from __future__ import annotations

from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model

from .models import User as UserType

User = get_user_model()


class UserAdminChangeForm(auth_forms.UserChangeForm[UserType]):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(auth_forms.UserCreationForm[UserType]):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
