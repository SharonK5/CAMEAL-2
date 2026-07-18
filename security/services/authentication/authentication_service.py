# security/services/authentication/authentication_service.py
from __future__ import annotations

from abc import abstractmethod

from security.services.base.security_context import SecurityContext
from security.services.base.security_result import SecurityResult
from security.services.base.service import Service


class AuthenticationService(Service):
    """
    Abstract base for authentication application services.
    """

    @property
    def security_domain(self) -> str:
        return "authentication"

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    @abstractmethod
    def authenticate(self, context: SecurityContext) -> SecurityResult:
        """Authenticate using a SecurityContext."""

    @abstractmethod
    def authenticate_user(self, username: str, credential: str) -> SecurityResult:
        """Authenticate a human user with password credentials."""

    @abstractmethod
    def authenticate_system(self, system_id: str, secret: str) -> SecurityResult:
        """Authenticate a system/service account."""

    @abstractmethod
    def authenticate_token(self, token: str) -> SecurityResult:
        """Authenticate using a token (e.g., JWT)."""

    @abstractmethod
    def authenticate_api_key(self, api_key: str) -> SecurityResult:
        """Authenticate using an API key."""

    # ------------------------------------------------------------------
    # Session
    # ------------------------------------------------------------------

    @abstractmethod
    def refresh_session(self, session_id: str) -> SecurityResult:
        """Refresh an existing session."""

    @abstractmethod
    def logout(self, session_id: str) -> SecurityResult:
        """Terminate a session."""

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    @abstractmethod
    def verify_identity(self, identity: str) -> SecurityResult:
        """Verify that an identity exists."""
