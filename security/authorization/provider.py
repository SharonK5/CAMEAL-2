# security/authorization/provider.py
"""
Base class for all authorization providers.

Provides a uniform contract for metadata, lifecycle, and health
across PermissionProvider, RoleProvider, ConstraintProvider, and
ObligationProvider.
"""

from typing import Any, Dict


class AuthorizationProvider:
    """
    Base class for all authorization providers.

    Attributes:
        PROVIDER_NAME: Unique identifier for the provider.
        PROVIDER_VERSION: Semantic version string.
    """

    PROVIDER_NAME = "AuthorizationProvider"
    PROVIDER_VERSION = "1.0.0"

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return self.PROVIDER_NAME

    @property
    def provider_version(self) -> str:
        """Return the provider version."""
        return self.PROVIDER_VERSION

    @property
    def metadata(self) -> Dict[str, Any]:
        """
        Return provider metadata for audit and diagnostics.

        Includes name, version, implementation class, and health status.

        Returns:
            Dict[str, Any]: Provider metadata.
        """
        return {
            "provider_name": self.provider_name,
            "provider_version": self.provider_version,
            "implementation": self.__class__.__name__,
            "healthy": self.health(),
        }

    def initialize(self) -> None:
        """
        Perform one-time setup (e.g., connect to external systems).
        Override if needed.
        """
        return None

    def shutdown(self) -> None:
        """
        Release resources and clean up.
        Override if needed.
        """
        return None

    def validate(self) -> None:
        """
        Validate configuration and dependencies.

        Raises:
            SecurityValidationError: If validation fails.
        """
        return None

    def health(self) -> bool:
        """
        Check the health of the provider.

        Returns:
            bool: True if healthy, False otherwise.
        """
        return True

    def clear_cache(self) -> None:
        """
        Clear any internal caches.
        Override if caching is used.
        """
        return None

    def reload(self) -> None:
        """
        Reload provider configuration or backing data.
        Override if needed.
        """
        return None
