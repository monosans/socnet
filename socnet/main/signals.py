from __future__ import annotations

from ..utils.pre_save_full_clean import pre_save_full_clean
from . import models

pre_save_full_clean(sender=models.Post)
pre_save_full_clean(sender=models.PostComment)
