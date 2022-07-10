from __future__ import annotations

from copy import deepcopy

from rest_framework.permissions import DjangoModelPermissions


class DjangoModelPermissionsWithViewPermissionCheck(DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map = deepcopy(self.perms_map)
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]
