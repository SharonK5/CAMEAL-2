# kernel/providers/authentication/auth_provider.py
"""
Authentication provider abstraction.
"""

from abc import abstractmethod
from typing import Any, Dict, Optional

from ..base.provider import Provider


class AuthProvider(Provider):
    """
    Base interface for authentication providers.

    Authentication providers handle:
        - User authentication (verifying credentials)
        - Token generation and verification
        - Authorization (checking permissions)
        - Session management (optional)

    Examples of implementations:
        - JWT (JSON Web Tokens)
        - API Key
        - OAuth2 (with external provider)
        - LDAP / Active Directory
        - Database-backed user/password

    All auth providers must support:
        - Authenticating a user with credentials
        - Generating a token (JWT, session ID, etc.)
        - Verifying a token
        - (Optional) Authorization/permission checks
    """

    @abstractmethod
    def get(self) -> Any:
        """Return the underlying auth client or configuration."""
        pass

    @abstractmethod
    def authenticate(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Authenticate a user or system.

        Args:
            credentials: Dict containing authentication credentials.
                         Common keys: "username", "password", "api_key", "token".

        Returns:
            A dict containing authentication result:
                - success (bool)
                - user_id (str, optional)
                - metadata (dict, optional)

        Raises:
            ProviderError: If authentication fails.
        """
        pass

    @abstractmethod
    def generate_token(self, user_id: str, payload: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate an authentication token for a user.

        Args:
            user_id: The user identifier.
            payload: Optional additional claims.

        Returns:
            The generated token string.

        Raises:
            ProviderError: If token generation fails.
        """
        pass

    @abstractmethod
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify a token and return its payload.

        Args:
            token: The token string.

        Returns:
            A dict containing:
                - valid (bool)
                - user_id (str, optional)
                - payload (dict, optional)

        Raises:
            ProviderError: If verification fails due to errors.
        """
        pass

    @abstractmethod
    def revoke_token(self, token: str) -> None:
        """
        Revoke a token (invalidate it).

        Args:
            token: The token string.

        Raises:
            ProviderError: If revocation fails.
        """
        pass

    @abstractmethod
    def authorize(self, user_id: str, resource: str, action: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if a user has permission to perform an action on a resource.

        This is a simple authorization check. More complex providers
        may support roles, policies, or external authorization services.

        Args:
            user_id: The user identifier.
            resource: The resource (e.g., "document:123", "workflow:build").
            action: The action (e.g., "read", "write", "execute").
            context: Optional context for authorization decisions.

        Returns:
            True if authorized, False otherwise.

        Raises:
            ProviderError: If the authorization check fails.
        """
        pass
