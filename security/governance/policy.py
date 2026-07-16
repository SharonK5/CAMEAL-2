"""
===============================================================================
Module: security.policy

Immutable authorization policy definition.

A Policy defines the conditions under which a permission may be granted.
Policies are evaluated by the PolicyEngine.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet

from security.identity.permissions import Permission
from security.identity.roles import Role


@dataclass(slots=True, frozen=True)
class Policy:
    """
    Immutable authorization policy.
    """

    name: str

    roles: FrozenSet[Role]

    permissions: FrozenSet[Permission]

    enabled: bool = True

    description: str = ""

    def allows_role(self, role: Role) -> bool:
        """
        Return True if the role is covered by this policy.
        """
        return role in self.roles

    def allows_permission(
        self,
        permission: Permission,
    ) -> bool:
        """
        Return True if the permission is granted by this policy.
        """
        return permission in self.permissions
