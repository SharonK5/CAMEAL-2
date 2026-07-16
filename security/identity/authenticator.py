"""
===============================================================================
Module: security.authenticator

Authentication service for CAMEAL.

Responsibilities
----------------
- Authenticate credentials
- Verify account state
- Update authentication metadata
- Produce AuthenticationResult

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from datetime import UTC, datetime

from .authentication_request import AuthenticationRequest
from .authentication_result import AuthenticationResult
from security.integrity.hashing import HashingService
from .identity_provider import IdentityProvider


class Authenticator:
    """
    Stateless authentication service.
    """

    MAX_FAILED_ATTEMPTS = 5

    def __init__(
        self,
        provider: IdentityProvider,
        hashing: HashingService,
    ) -> None:

        self._provider = provider
        self._hashing = hashing

    def authenticate(
        self,
        request: AuthenticationRequest,
    ) -> AuthenticationResult:
        """
        Authenticate a user.
        """

        identity = self._provider.get(request.username)

        if identity is None:
            return AuthenticationResult(
                success=False,
                message="Invalid username or password.",
            )

        if not identity.enabled:
            return AuthenticationResult(
                success=False,
                message="Account disabled.",
            )

        if identity.locked:
            return AuthenticationResult(
                success=False,
                message="Account locked.",
            )

        # Verify password – using the correct method name
        if not self._hashing.verify_password(
            request.password,
            identity.password_hash,
        ):
            identity.failed_attempts += 1

            if identity.failed_attempts >= self.MAX_FAILED_ATTEMPTS:
                identity.locked = True

            self._provider.save(identity)

            return AuthenticationResult(
                success=False,
                message="Invalid username or password.",
            )

        # --- Password correct ---
        identity.failed_attempts = 0
        identity.last_login = datetime.now(UTC)
        self._provider.save(identity)

        return AuthenticationResult(
            success=True,
            user=identity.user,
            message="Authentication successful.",
        )
