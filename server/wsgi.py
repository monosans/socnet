"""https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/"""
from __future__ import annotations

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings.local")
application = get_wsgi_application()
