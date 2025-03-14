from __future__ import annotations

from django.urls import path

from socnet.api.views import api

urlpatterns = [path("", api.urls)]
