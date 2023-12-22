# https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
from __future__ import annotations

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
application = get_wsgi_application()
