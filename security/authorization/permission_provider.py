# security/authorization/permission_provider.py
"""
Permission provider interface and default implementation.
"""

from typing import Tuple

from .models import Permission, AuthorizationRequest
from .provider import AuthorizationProvider


class PermissionProvider(AuthorizationProvider):
    """
    Provides effective permissions for a given authorization request.
    """

    PROVIDER_NAME = "DefaultPermissionProvider"
    PROVIDER_VERSION = "1.0.0"

    def get_permissions(self, request: AuthorizationRequest) -> Tuple[Permission, ...]:
        """
        Retrieve all permissions applicable to the request.

        Implementations may consider identity, resource, operation, metadata,
        resource type, and roles.

        Args:
            request: The authorization request.

        Returns:
            Tuple[Permission, ...]: A tuple of Permission objects.
        """
        raise NotImplementedError(
            f"{self.provider_name}.get_permissions() must be implemented."
        )


class DefaultPermissionProvider(PermissionProvider):
    """
    Default stub provider for testing and development.

    Always returns a synthetic permission 'default.read'.
    """

    PROVIDER_NAME = "DefaultPermissionProvider"
    PROVIDER_VERSION = "1.0.0"

    def get_permissions(self, request: AuthorizationRequest) -> Tuple[Permission, ...]:
        return (
            Permission(
                name="default.read",
                description="Default synthetic read permission.",
            ),
        )
