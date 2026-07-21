import logging
# kernel/providers/authentication/implementations/api_key_provider.py
"""
API Key authentication provider.

Simple provider that validates API keys against a stored set.
"""

import os
import hashlib
from typing import Any, Dict, Optional, Set

from ..auth_provider import AuthProvider
from kernel.lifecycle import HealthStatus
from ...base.exceptions import ProviderInitializationError, ProviderError

logger = logging.getLogger(__name__)


class APIKeyProvider(AuthProvider):
    """
    API Key authentication provider.

    This provider validates API keys against a configured set of allowed keys.

    Usage:
        provider = APIKeyProvider(valid_keys={"key1": "user1", "key2": "user2"})
        provider.start()
        result = provider.authenticate({"api_key": "key1"})
        # result["user_id"] == "user1"
        provider.stop()
    """

    def __init__(self, valid_keys: Optional[Dict[str, str]] = None) -> None:
        """
        Initialize the API Key provider.

        Args:
            valid_keys: Dict mapping api_key -> user_id.
        """
        self._valid_keys = valid_keys or {}
        self._initialized = False
        self._rate_limits = {}  # Optional: track rate limits per key

    def get(self) -> Any:
        """Return the valid keys dictionary."""
        return self._valid_keys

    def start(self) -> None:
        """Initialize the API Key provider."""
        self._initialized = True
        logger.info(f"API Key provider initialized with {len(self._valid_keys)} keys")

    def stop(self) -> None:
        """Clean up the API Key provider."""
        self._initialized = False

    def health(self) -> HealthStatus:
        """Check if the API Key provider is healthy."""
        if not self._initialized:
            return HealthStatus.UNHEALTHY
        return HealthStatus.HEALTHY

    def authenticate(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Authenticate using an API key.

        Expects: {"api_key": "..."}

        Args:
            credentials: Dict with "api_key" key.

        Returns:
            Dict with authentication result.

        Raises:
            ProviderError: If authentication fails.
        """
        if not self._initialized:
            raise ProviderError("Provider not initialized")

        api_key = credentials.get("api_key")
        if not api_key:
            return {"success": False, "metadata": {"error": "Missing api_key"}}

        user_id = self._valid_keys.get(api_key)
        if user_id:
            return {
                "success": True,
                "user_id": user_id,
                "metadata": {"method": "api_key"},
            }
        else:
            return {"success": False, "metadata": {"error": "Invalid API key"}}

    def generate_token(self, user_id: str, payload: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate an API key for a user.

        Note: This is not typically used for API key providers, but we implement
        it for interface compliance. It generates a random key.

        Args:
            user_id: The user identifier.
            payload: Optional additional data.

        Returns:
            The generated API key string.

        Raises:
            ProviderError: If generation fails.
        """
        import secrets

        # Generate a random key
        key = secrets.token_urlsafe(32)
        self._valid_keys[key] = user_id
        return key

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify an API key.

        For API key providers, this is the same as authenticate.

        Args:
            token: The API key string.

        Returns:
            Dict with verification result.
        """
        result = self.authenticate({"api_key": token})
        if result.get("success"):
            return {"valid": True, "user_id": result.get("user_id")}
        else:
            return {"valid": False, "error": result.get("metadata", {}).get("error")}

    def revoke_token(self, token: str) -> None:
        """
        Revoke an API key.

        Args:
            token: The API key string.

        Raises:
            ProviderError: If revocation fails.
        """
        if token in self._valid_keys:
            del self._valid_keys[token]
            logger.info(f"Revoked API key: {token[:8]}...")
        else:
            logger.warning(f"Attempted to revoke non-existent API key: {token[:8]}...")

    def authorize(self, user_id: str, resource: str, action: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Authorize a user.

        For API key auth, we allow all actions by default.
        """
        return True

    def add_key(self, key: str, user_id: str) -> None:
        """Add a new API key."""
        self._valid_keys[key] = user_id
        logger.info(f"Added API key for user {user_id}")

    def remove_key(self, key: str) -> None:
        """Remove an API key."""
        if key in self._valid_keys:
            del self._valid_keys[key]
            logger.info(f"Removed API key {key[:8]}...")
