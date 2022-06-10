from captcha.fields import CaptchaField, CaptchaTextInput
from django.contrib.auth import forms, get_user_model

from .models import User as UserType

User = get_user_model()


class _CaptchaTextInput(CaptchaTextInput):  # type: ignore[misc]
    template_name = "users/inc/captcha.html"


class UserCreationForm(forms.UserCreationForm[UserType]):
    captcha = CaptchaField(widget=_CaptchaTextInput)

    class Meta(forms.UserCreationForm.Meta):
        model = User
