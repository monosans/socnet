from __future__ import annotations

from copy import deepcopy
from typing import ClassVar

from rest_framework.permissions import DjangoModelPermissions


class ActualDjangoModelPermissions(DjangoModelPermissions):
    perms_map: ClassVar[dict[str, list[str]]] = deepcopy(
        DjangoModelPermissions.perms_map
    )
    perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]  # noqa: RUF012
    perms_map["HEAD"] = perms_map["GET"].copy()
