from __future__ import annotations

from rest_framework import fields, generics

# Monkeypatch to make generics work at runtime
for cls in (fields.Field, generics.GenericAPIView):
    cls.__class_getitem__ = classmethod(  # type: ignore[attr-defined]
        lambda cls, *args, **kwargs: cls
    )
