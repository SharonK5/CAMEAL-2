# kernel/context/security_context.py
"""
Security context – identity, roles, permissions.
"""

from dataclasses import dataclass, field
from typing import Dict, Tuple

from .exceptions import ContextValidationError


@dataclass(frozen=True)
class SecurityContext:
    """
    Immutable security context.

    Attributes:
        identity: Principal identity.
        roles: Assigned roles.
        permissions: Granted permissions.
        authenticated: Whether the identity is authenticated.
        metadata: Additional security metadata.
    """

    identity: str = ""
    roles: Tuple[str, ...] = ()
    permissions: Tuple[str, ...] = ()
    authenticated: bool = False
    metadata: Dict[str, str] = field(default_factory=dict)

    def has_role(self, role: str) -> bool:
        """Check if a role is present."""
        return role in self.roles

    def has_permission(self, permission: str) -> bool:
        """Check if a permission is present."""
        return permission in self.permissions

    def to_dict(self) -> Dict[str, str]:
        return {
            "identity": self.identity,
            "roles": list(self.roles),
            "permissions": list(self.permissions),
            "authenticated": str(self.authenticated),
            **self.metadata,
        }
