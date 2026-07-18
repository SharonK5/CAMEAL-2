# security/services/policy/policy_service.py
from __future__ import annotations

from abc import abstractmethod

from security.services.base.security_context import SecurityContext
from security.services.base.security_decision import SecurityDecision
from security.services.base.service import Service


class PolicyService(Service):
    """
    Base Policy Service.

    Orchestrates policy evaluation by coordinating the PolicyEngine
    and PolicyProvider implementations. Converts domain PolicyResult
    objects into framework-level SecurityDecision objects.

    Concrete implementations should remain independent of the execution
    pipeline so they can be reused by:

        • Query Engine
        • REST API
        • CLI
        • RAG Engine
        • Enterprise API
        • Future microservices
    """

    @property
    def security_domain(self) -> str:
        return "policy"

    # ---------------------------------------------------------
    # Core evaluation
    # ---------------------------------------------------------

    @abstractmethod
    def evaluate(self, context: SecurityContext) -> SecurityDecision:
        """
        Evaluate all applicable policies against the given context.

        Returns a SecurityDecision.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Policy management
    # ---------------------------------------------------------

    @abstractmethod
    def load_policies(self) -> None:
        """
        Load all available policies from the configured provider.
        """
        raise NotImplementedError

    @abstractmethod
    def reload_policies(self) -> None:
        """
        Reload policies from the configured provider.
        """
        raise NotImplementedError

    @abstractmethod
    def validate_policies(self) -> None:
        """
        Validate all loaded policies.
        """
        raise NotImplementedError

    @abstractmethod
    def list_policies(self) -> tuple[str, ...]:
        """
        Return the names of all loaded policies.
        """
        raise NotImplementedError

    @abstractmethod
    def clear_cache(self) -> None:
        """
        Clear any cached policy state.
        """
        raise NotImplementedError
