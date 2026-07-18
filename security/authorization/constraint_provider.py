# security/authorization/constraint_provider.py
"""
Constraint provider interface and default implementation.
"""

from typing import Tuple

from .models import Constraint, AuthorizationRequest
from .provider import AuthorizationProvider


class ConstraintProvider(AuthorizationProvider):
    """
    Provides constraints for a given authorization request.
    """

    PROVIDER_NAME = "DefaultConstraintProvider"
    PROVIDER_VERSION = "1.0.0"

    def get_constraints(self, request: AuthorizationRequest) -> Tuple[Constraint, ...]:
        """
        Retrieve all constraints applicable to the request.

        Args:
            request: The authorization request.

        Returns:
            Tuple[Constraint, ...]: A tuple of Constraint objects.
        """
        raise NotImplementedError(
            f"{self.provider_name}.get_constraints() must be implemented."
        )


class DefaultConstraintProvider(ConstraintProvider):
    """
    Default stub provider for testing and development.

    Always returns an empty tuple (no constraints).
    """

    PROVIDER_NAME = "DefaultConstraintProvider"
    PROVIDER_VERSION = "1.0.0"

    def get_constraints(self, request: AuthorizationRequest) -> Tuple[Constraint, ...]:
        return ()
