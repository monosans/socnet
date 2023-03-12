from __future__ import annotations

from copy import deepcopy

from rest_framework.permissions import DjangoModelPermissions


class ActualDjangoModelPermissions(DjangoModelPermissions):
    perms_map = deepcopy(DjangoModelPermissions.perms_map)
    perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]
    perms_map["HEAD"] = perms_map["GET"].copy()
