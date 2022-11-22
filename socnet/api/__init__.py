from __future__ import annotations

from rest_framework.fields import Field as _Field
from rest_framework.generics import GenericAPIView as _GenericAPIView

# Monkeypatch to make generics work at runtime
for _cls in (_Field, _GenericAPIView):
    _cls.__class_getitem__ = classmethod(  # type: ignore[attr-defined]
        lambda cls, *args, **kwargs: cls
    )
