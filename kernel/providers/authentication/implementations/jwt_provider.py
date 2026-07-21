import logging
# kernel/providers/authentication/implementations/jwt_provider.py
"""
JWT (JSON Web Token) authentication provider.

Uses the PyJWT library for token generation and verification.
"""

import os
from typing import Any, Dict, Optional
import jwt
import time
from datetime import datetime, timedelta

from ..auth_provider import AuthProvider
from kernel.lifecycle import HealthStatus
from ...base.exceptions import ProviderInitializationError, ProviderError

logger = logging.getLogger(__name__)


class JWTProvider(AuthProvider):
    """
    JWT-based authentication provider.

    This provider uses JSON Web Tokens for authentication.
    Tokens are signed with a secret key and can include custom claims.

    Features:
        - Configurable token expiration
        - Algorithm support (HS256, RS256, etc.)
        - Refresh tokens (optional)

    Usage:
        provider = JWTProvider(secret="my-secret", algorithm="HS256")
        provider.start()
        token = provider.generate_token("user123", {"role": "admin"})
        payload = provider.verify_token(token)
        provider.stop()
    """

    def __init__(
        self,
        secret: Optional[str] = None,
        algorithm: str = "HS256",
        expiration_minutes: int = 60,
        refresh_expiration_minutes: int = 1440,  # 24 hours
    ) -> None:
        """
        Initialize the JWT provider.

        Args:
            secret: The secret key for signing tokens (defaults to JWT_SECRET env var).
            algorithm: The signing algorithm (default: HS256).
            expiration_minutes: Token expiration in minutes (default: 60).
            refresh_expiration_minutes: Refresh token expiration in minutes (default: 1440).
        """
        self._secret = secret or os.environ.get("JWT_SECRET")
        if not self._secret:
            raise ValueError("JWT secret not provided and not found in environment")

        self._algorithm = algorithm
        self._expiration_minutes = expiration_minutes
        self._refresh_expiration_minutes = refresh_expiration_minutes
        self._revoked_tokens = set()
        self._initialized = False

    def get(self) -> Any:
        """Return the JWT configuration (secret, algorithm)."""
        return {"secret": self._secret, "algorithm": self._algorithm}

    def start(self) -> None:
        """Initialize the JWT provider."""
        self._initialized = True
        logger.info("JWT provider initialized")

    def stop(self) -> None:
        """Clean up the JWT provider."""
        self._revoked_tokens.clear()
        self._initialized = False

    def health(self) -> HealthStatus:
        """Check if the JWT provider is healthy."""
        if not self._initialized:
            return HealthStatus.UNHEALTHY
        if not self._secret:
            return HealthStatus.UNHEALTHY
        return HealthStatus.HEALTHY

    def authenticate(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Authenticate a user with username/password or other credentials.

        This implementation expects either:
            - {"username": "...", "password": "..."}
            - {"token": "..."}  # Existing token

        In a real implementation, you would verify against a user database.
        For this provider, we accept any username with a non-empty password.

        Args:
            credentials: Dict with authentication details.

        Returns:
            Dict with authentication result.

        Raises:
            ProviderError: If authentication fails.
        """
        if "username" in credentials and "password" in credentials:
            # For demo: accept any non-empty username and password
            if credentials["username"] and credentials["password"]:
                return {
                    "success": True,
                    "user_id": credentials["username"],
                    "metadata": {"method": "password"},
                }
        elif "token" in credentials:
            try:
                payload = self.verify_token(credentials["token"])
                if payload.get("valid"):
                    return {
                        "success": True,
                        "user_id": payload.get("user_id"),
                        "metadata": {"method": "token"},
                    }
            except Exception:
                pass

        return {"success": False, "metadata": {"error": "Invalid credentials"}}

    def generate_token(self, user_id: str, payload: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a JWT for the user.

        Args:
            user_id: The user identifier.
            payload: Additional claims to include in the token.

        Returns:
            The JWT string.

        Raises:
            ProviderError: If token generation fails.
        """
        if not self._initialized:
            raise ProviderError("Provider not initialized")

        now = time.time()
        payload = payload or {}
        payload.update({
            "sub": user_id,
            "iat": now,
            "exp": now + (self._expiration_minutes * 60),
            "iss": "cameal-kernel",
        })

        try:
            token = jwt.encode(payload, self._secret, algorithm=self._algorithm)
            return token
        except Exception as e:
            raise ProviderError(f"Failed to generate JWT: {e}") from e

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify a JWT and return its payload.

        Args:
            token: The JWT string.

        Returns:
            Dict with verification result.

        Raises:
            ProviderError: If verification fails.
        """
        if not self._initialized:
            raise ProviderError("Provider not initialized")

        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms=[self._algorithm],
                issuer="cameal-kernel",
            )
            user_id = payload.get("sub")

            # Check if revoked
            if token in self._revoked_tokens:
                return {"valid": False, "error": "Token revoked"}

            return {
                "valid": True,
                "user_id": user_id,
                "payload": payload,
            }
        except jwt.ExpiredSignatureError:
            return {"valid": False, "error": "Token expired"}
        except jwt.InvalidTokenError as e:
            return {"valid": False, "error": f"Invalid token: {e}"}

    def revoke_token(self, token: str) -> None:
        """
        Revoke a JWT.

        Args:
            token: The JWT string.

        Raises:
            ProviderError: If revocation fails.
        """
        if not self._initialized:
            raise ProviderError("Provider not initialized")

        self._revoked_tokens.add(token)

    def authorize(self, user_id: str, resource: str, action: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Authorize a user for a resource/action.

        This is a simple implementation. For more complex authorization,
        you would integrate with an external policy engine or RBAC.

        Args:
            user_id: The user identifier.
            resource: The target resource.
            action: The action to perform.
            context: Optional context.

        Returns:
            True if authorized, False otherwise.
        """
        # For demonstration: allow all actions by default
        # In production, implement proper authorization logic
        return True
