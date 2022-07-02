from django.contrib.auth import forms, get_user_model

from .models import User as UserType

User = get_user_model()


class UserCreationForm(forms.UserCreationForm[UserType]):
    class Meta(forms.UserCreationForm.Meta):
        model = User
