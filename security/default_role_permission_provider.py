"""
===============================================================================
Module: security.default_role_permission_provider

Default Role → Permission mapping for CAMEAL.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .permissions import Permission
from .role_permission_provider import RolePermissionProvider
from .roles import Role


class DefaultRolePermissionProvider(RolePermissionProvider):
    """
    Default built-in RBAC policy.
    """

    def __init__(self) -> None:

        self._mapping: dict[Role, set[Permission]] = {

            Role.SYSTEM_ADMIN: set(Permission),

            Role.AI_ADMINISTRATOR: {
                Permission.READ,
                Permission.WRITE,
                Permission.QUERY,
                Permission.ANALYZE,
                Permission.CONFIGURE,
                Permission.REVIEW,
            },

            Role.GOVERNANCE_OFFICER: {
                Permission.READ,
                Permission.WRITE,
                Permission.REVIEW,
                Permission.GOVERN,
                Permission.QUERY,
            },

            Role.RESEARCHER: {
                Permission.READ,
                Permission.QUERY,
                Permission.ANALYZE,
                Permission.EXPORT,
            },

            Role.ANALYST: {
                Permission.READ,
                Permission.QUERY,
                Permission.ANALYZE,
            },

            Role.OPERATOR: {
                Permission.READ,
                Permission.WRITE,
                Permission.INGEST,
            },

            Role.API_CLIENT: {
                Permission.READ,
                Permission.QUERY,
            },

            Role.REVIEWER: {
                Permission.READ,
                Permission.REVIEW,
            },

            Role.GUEST: {
                Permission.READ,
            },
        }

    def permissions_for(
        self,
        role: Role,
    ) -> set[Permission]:

        return self._mapping.get(role, set())
