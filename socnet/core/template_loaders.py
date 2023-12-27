from __future__ import annotations

from django.template.loaders.app_directories import (
    Loader as AppDirectoriesLoader,
)
from django.template.loaders.filesystem import Loader as FilesystemLoader

from socnet_rs import minify_template

from .decorators import process_returned_value

minify_returned_value = process_returned_value(minify_template)


class MinifiedFilesystemLoader(FilesystemLoader):
    get_contents = minify_returned_value(FilesystemLoader.get_contents)


class MinifiedAppDirectoriesLoader(AppDirectoriesLoader):
    get_contents = minify_returned_value(AppDirectoriesLoader.get_contents)
