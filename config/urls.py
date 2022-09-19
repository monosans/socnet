"""https://docs.djangoproject.com/en/4.1/topics/http/urls/"""
from __future__ import annotations

from allauth import urls as allauth_urls
from django.conf import settings
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.urls import include, path
from django.views.generic import TemplateView

from socnet.api import urls as api_urls
from socnet.core.views import admin_site_login_view
from socnet.main import urls as main_urls
from socnet.messenger import urls as messenger_urls

# https://django-allauth.readthedocs.io/en/latest/advanced.html#admin
admin.site.login = admin_site_login_view  # type: ignore[assignment]

urlpatterns = [
    path("admin/doc/", include(admindocs_urls)),
    path("admin/", admin.site.urls),
    path("accounts/", include(allauth_urls)),
    path("api/", include(api_urls)),
    path("chat/", include(messenger_urls)),
    path("", include(main_urls)),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt", content_type="text/plain"
        ),
    ),
]

if settings.DEBUG:  # pragma: no cover
    # pylint: disable-next=ungrouped-imports
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += staticfiles_urlpatterns()

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
            *urlpatterns,
        ]
