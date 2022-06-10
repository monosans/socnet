"""https://docs.djangoproject.com/en/4.0/topics/http/urls/"""
from captcha import urls as captcha_urls
from defender import urls as defender_urls
from django.conf import settings
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.urls import include, path
from django.views.generic import TemplateView

from .apps.api import urls as api_urls
from .apps.main import urls as main_urls
from .apps.messenger import urls as messenger_urls
from .apps.users import urls as users_urls

urlpatterns = [
    path("admin/defender/", include(defender_urls)),
    path("admin/doc/", include(admindocs_urls)),
    path("admin/", admin.site.urls),
    path("chat/", include(messenger_urls)),
    path("", include(users_urls)),
    path("", include(main_urls)),
    path("api/v1/", include(api_urls)),
    path("captcha/", include(captcha_urls)),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="txt/robots.txt", content_type="text/plain"
        ),
    ),
]
if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        *urlpatterns,
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
