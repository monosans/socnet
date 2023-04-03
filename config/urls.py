"""https://docs.djangoproject.com/en/4.2/topics/http/urls/"""
from __future__ import annotations

from typing import List, Union

from allauth import urls as allauth_urls
from allauth_2fa import urls as allauth_2fa_urls
from django.conf import settings
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.urls import URLPattern, URLResolver, include, path

from socnet.api import urls as api_urls
from socnet.blog import urls as blog_urls
from socnet.core import urls as core_urls, views as core_views
from socnet.messenger import urls as messenger_urls
from socnet.users import urls as users_urls

# https://django-allauth.readthedocs.io/en/latest/advanced.html#admin
admin.site.login = core_views.admin_site_login_view  # type: ignore[assignment]

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("admin/doc/", include(admindocs_urls)),
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
    path("messenger/", include(messenger_urls)),
    path("", include(allauth_2fa_urls)),
    path("", include(allauth_urls)),
    path("", include(core_urls)),
    path("", include(blog_urls)),
    path("", include(users_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls)), *urlpatterns]
