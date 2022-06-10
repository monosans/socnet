import os
from pathlib import Path
from typing import Union

import django_stubs_ext

# Monkeypatching Django, so stubs will work for all generics,
# see: https://github.com/typeddjango/django-stubs
django_stubs_ext.monkeypatch()

os.environ.setdefault("DJANGO_ENV", "development")

MEDIA_ROOT: Union[Path, str]

from .common import *

if os.environ["DJANGO_ENV"] == "development":
    from .development import *
else:
    from .production import *
