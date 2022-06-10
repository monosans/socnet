"""https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
application = get_wsgi_application()
