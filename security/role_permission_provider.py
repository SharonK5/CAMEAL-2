from __future__ import annotations

from abc import ABC, abstractmethod

from .permissions import Permission
from .roles import Role


class RolePermissionProvider(ABC):
    """
    Contract for role-permission providers.
    """

    @abstractmethod
    def permissions_for(
        self,
        role: Role,
    ) -> set[Permission]:
        """
        Return the permissions granted to a role.
        """
        raise NotImplementedError
