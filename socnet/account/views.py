from __future__ import annotations

from typing import Any, Callable, Type

from allauth.account import views as allauth_views
from allauth_2fa import views as allauth_2fa_views
from django.forms import BaseForm
from django.http import HttpResponseBase
from django.views.generic.edit import BaseFormView

from . import forms


def monkeypatch_form_class(
    view: Type[BaseFormView[Any]], form_class: Type[BaseForm]
) -> Callable[..., HttpResponseBase]:
    new_view: Type[BaseFormView[Any]] = type(
        view.__name__, (view,), {"form_class": form_class}
    )
    return new_view.as_view()


login = monkeypatch_form_class(allauth_views.LoginView, forms.LoginForm)
signup = monkeypatch_form_class(allauth_views.SignupView, forms.SignupForm)
password_reset = monkeypatch_form_class(
    allauth_views.PasswordResetView, forms.ResetPasswordForm
)
email = monkeypatch_form_class(allauth_views.EmailView, forms.AddEmailForm)

two_factor_setup = monkeypatch_form_class(
    allauth_2fa_views.TwoFactorSetup, forms.TOTPDeviceForm
)
