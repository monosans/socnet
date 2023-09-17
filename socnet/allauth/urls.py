from __future__ import annotations

from allauth.account.urls import urlpatterns as allauth_urlpatterns
from allauth.mfa.urls import urlpatterns as mfa_urlpatterns
from django.urls import include, path

urlpatterns = [
    path("", include(allauth_urlpatterns)),
    path("totp/", include(mfa_urlpatterns)),
]
