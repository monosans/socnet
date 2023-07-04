from __future__ import annotations

from allauth.account.urls import urlpatterns as allauth_urlpatterns
from allauth_2fa.urls import urlpatterns as allauth_2fa_urlpatterns
from django.urls import path, include

urlpatterns = [
    path("", include(allauth_urlpatterns)),
    path("totp/", include(allauth_2fa_urlpatterns)),
]
