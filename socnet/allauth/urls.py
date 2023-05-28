from __future__ import annotations

from allauth.account.urls import urlpatterns as allauth_urlpatterns
from allauth_2fa.urls import urlpatterns as allauth_2fa_urlpatterns
from django.urls import path, re_path
from django.urls.resolvers import RegexPattern

from . import views

_allauth_views_overrides = {
    "account_login": views.login,
    "account_signup": views.signup,
    "account_email": views.email,
    "account_reset_password": views.password_reset,
}
urlpatterns = [
    (re_path if isinstance(url.pattern, RegexPattern) else path)(
        str(url.pattern),
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
for url in allauth_2fa_urlpatterns:
    route = _allauth_2fa_pattern_overrides.get(url.name, url.pattern)
    urlpatterns.append(
        (re_path if isinstance(route, RegexPattern) else path)(
            str(route),
            _allauth_2fa_views_overrides.get(url.name, url.callback),
            kwargs=url.default_args,
            name=url.name,
        )
    )
