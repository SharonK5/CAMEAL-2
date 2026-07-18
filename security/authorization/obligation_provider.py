# security/authorization/obligation_provider.py
"""
Obligation provider interface and default implementation.
"""

from typing import Tuple

from .models import Obligation, AuthorizationRequest
from .provider import AuthorizationProvider


class ObligationProvider(AuthorizationProvider):
    """
    Provides obligations for a given authorization request.
    """

    PROVIDER_NAME = "DefaultObligationProvider"
    PROVIDER_VERSION = "1.0.0"

    def get_obligations(self, request: AuthorizationRequest) -> Tuple[Obligation, ...]:
        """
        Retrieve all obligations applicable to the request.

        Args:
            request: The authorization request.

        Returns:
            Tuple[Obligation, ...]: A tuple of Obligation objects.
        """
        raise NotImplementedError(
            f"{self.provider_name}.get_obligations() must be implemented."
        )


class DefaultObligationProvider(ObligationProvider):
    """
    Default stub provider for testing and development.

    Always returns an empty tuple (no obligations).
    """

    PROVIDER_NAME = "DefaultObligationProvider"
    PROVIDER_VERSION = "1.0.0"

    def get_obligations(self, request: AuthorizationRequest) -> Tuple[Obligation, ...]:
        return ()
