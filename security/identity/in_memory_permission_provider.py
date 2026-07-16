# security/in_memory_permission_provider.py

from typing import Set
from .role_permission_provider import RolePermissionProvider
from .roles import Role
from .permissions import Permission

class InMemoryPermissionProvider(RolePermissionProvider):
    """Simple provider with a hardcoded mapping (same as before)."""

    def __init__(self) -> None:
        self._mapping: dict[Role, Set[Permission]] = {
            Role.SYSTEM_ADMIN: set(Permission),      # all permissions
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

    def permissions_for(self, role: Role) -> Set[Permission]:
        return self._mapping.get(role, set())
