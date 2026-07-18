# security/authorization/authorizer.py
from abc import ABC, abstractmethod
from .models import AuthorizationRequest, AuthorizationResult


class Authorizer(ABC):
    """
    Core authorization engine interface.

    Implementations evaluate authorization requests and return decisions.
    All engines should expose health and validation methods for consistency
    with the CAMEAL framework.
    """

    @abstractmethod
    def evaluate(self, request: AuthorizationRequest) -> AuthorizationResult:
        """
        Evaluate an authorization request.

        Args:
            request: The request to evaluate.

        Returns:
            AuthorizationResult: The authorization decision.
        """
        pass

    @abstractmethod
    def health(self) -> bool:
        """Return True if the engine is healthy."""
        pass

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the engine's configuration.

        Raises:
            SecurityValidationError: If validation fails.
        """
        pass
