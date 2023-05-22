from __future__ import annotations

from io import BytesIO
from typing import Any, Type, TypeVar

from django.core.files.base import ContentFile, File
from django.db.models import CharField, Field, ImageField, TextField
from django.db.models.fields.files import ImageFieldFile
from PIL import Image, ImageOps

from socnet_rs import normalize_str

from . import decorators

TField = TypeVar("TField", bound=Field[Any, Any])


def create_normalized_str_field(field: Type[TField]) -> Type[TField]:
    return type(
        f"Normalized{field.__name__}",
        (field,),
        {"clean": decorators.process_returned_value(normalize_str)(field.clean)},
    )


NormalizedCharField = create_normalized_str_field(CharField)
NormalizedTextField = create_normalized_str_field(TextField)


class WebpImageFieldFile(ImageFieldFile):
    def save(
        self, name: str, content: File[bytes], save: bool = True  # noqa: FBT001
    ) -> None:
        if content.file is None:
            return super().save(name, content, save)
        content.file.seek(0)
        image = ImageOps.exif_transpose(Image.open(content.file))
        with BytesIO() as buffer:
            image.save(buffer, "WEBP")
            webp_data = buffer.getvalue()
        webp_file = ContentFile(webp_data)
        return super().save(name, webp_file, save)


class WebpImageField(ImageField):
    attr_class = WebpImageFieldFile
