from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING

from django.core.files.base import ContentFile
from django.db.models import (
    CharField,
    DateTimeField,
    Field,
    ImageField,
    TextField,
)
from django.db.models.fields.files import ImageFieldFile
from django.utils import timezone
from PIL import Image, ImageOps
from typing_extensions import Any, TypeVar, override

from socnet_rs import normalize_str

from . import decorators

if TYPE_CHECKING:
    from django.core.files.base import File
    from django.db.models import Model

T_contra = TypeVar("T_contra", contravariant=True)
T_co = TypeVar("T_co", covariant=True)
TField = TypeVar("TField", bound=Field[Any, Any])


def create_normalized_str_field(field: type[TField]) -> type[TField]:
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
    @decorators.copy_type_hints(DateTimeField.__init__)
    def __init__(self, **kwargs: Any) -> None:
        kwargs["auto_now"] = True
        kwargs["auto_now_add"] = False
        kwargs["null"] = True
        super().__init__(**kwargs)

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
