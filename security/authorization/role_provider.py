# security/authorization/role_provider.py
"""
Role provider interface and default implementation.
"""

from typing import Tuple

from .models import Role, AuthorizationRequest
from .provider import AuthorizationProvider


class RoleProvider(AuthorizationProvider):
    """
    Provides roles for a given authorization request.
    """

    PROVIDER_NAME = "DefaultRoleProvider"
    PROVIDER_VERSION = "1.0.0"

    def get_roles(self, request: AuthorizationRequest) -> Tuple[Role, ...]:
        """
        Retrieve all roles applicable to the request.

        Args:
            request: The authorization request.

        Returns:
            Tuple[Role, ...]: A tuple of Role objects.
        """
        raise NotImplementedError(
            f"{self.provider_name}.get_roles() must be implemented."
        )


class DefaultRoleProvider(RoleProvider):
    """
    Default stub provider for testing and development.

    Always returns a synthetic role 'default.user'.
    """

    PROVIDER_NAME = "DefaultRoleProvider"
    PROVIDER_VERSION = "1.0.0"

    def get_roles(self, request: AuthorizationRequest) -> Tuple[Role, ...]:
        return (
            Role(
                name="default.user",
                description="Default synthetic user role.",
                permissions=(Permission(name="default.read"),),
            ),
        )
