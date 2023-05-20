from __future__ import annotations

from allauth.account.urls import urlpatterns as allauth_urlpatterns
from allauth_2fa.urls import urlpatterns as allauth_2fa_urlpatterns
from django.urls import path

from . import views

_allauth_views_overrides = {
    "account_login": views.login,
    "account_signup": views.signup,
    "account_email": views.email,
    "account_reset_password": views.password_reset,
}
urlpatterns = [
    path(
        url.pattern,
        _allauth_views_overrides.get(url.name, url.callback),
        kwargs=url.default_args,
        name=url.name,
    )
    for url in allauth_urlpatterns
]

_allauth_2fa_pattern_overrides = {
    "two-factor-authenticate": "totp/authenticate/",
    "two-factor-setup": "totp/setup/",
    "two-factor-backup-tokens": "totp/backup/",
    "two-factor-remove": "totp/remove/",
}
_allauth_2fa_views_overrides = {"two-factor-setup": views.two_factor_setup}
urlpatterns += [
    path(
        _allauth_2fa_pattern_overrides.get(url.name, url.pattern),
        _allauth_2fa_views_overrides.get(url.name, url.callback),
        kwargs=url.default_args,
        name=url.name,
    )
    for url in allauth_2fa_urlpatterns
]
