from __future__ import annotations

from io import BytesIO
from typing import Type

from django.core.files.base import ContentFile, File
from django.db.models import (
    CharField,
    DateTimeField,
    Field,
    ImageField,
    Model,
    TextField,
)
from django.db.models.fields.files import ImageFieldFile
from django.utils import timezone
from PIL import Image, ImageOps
from typing_extensions import Any, TypeVar, override

from socnet_rs import normalize_str

from . import decorators
from .utils import copy_type_hints

T_contra = TypeVar("T_contra", contravariant=True)
T_co = TypeVar("T_co", covariant=True)
TField = TypeVar("TField", bound=Field[Any, Any])


def create_normalized_str_field(field: Type[TField]) -> Type[TField]:
    return type(
        f"Normalized{field.__name__}",
        (field,),
        {
            "clean": decorators.process_returned_value(normalize_str)(
                field.clean
            )
        },
    )


NormalizedCharField = create_normalized_str_field(CharField)
NormalizedTextField = create_normalized_str_field(TextField)


class NullAutoNowDateTimeField(DateTimeField[T_contra, T_co]):
    @copy_type_hints(DateTimeField.__init__)
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, auto_now=True, auto_now_add=False, null=True)

    @override
    def pre_save(self, model_instance: Model, add: bool) -> Any:
        value = None if add else timezone.now()
        setattr(model_instance, self.attname, value)
        return value


class WebpImageFieldFile(ImageFieldFile):
    @override
    def save(self, name: str, content: File[bytes], save: bool = True) -> None:
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
