from abc import ABC, abstractmethod
from typing import Tuple
from .models import PolicyRequest, PolicyResult, Policy


class PolicyEngine(ABC):
    @abstractmethod
    def evaluate(self, request: PolicyRequest) -> PolicyResult:
        pass

    @abstractmethod
    def load(self, policies: Tuple[Policy, ...]) -> None:
        """Load policies into the engine."""
        pass

    @abstractmethod
    def reload(self) -> None:
        """Reload policies from the configured source."""
        pass

    @abstractmethod
    def list_policies(self) -> Tuple[Policy, ...]:
        """Return all loaded policies."""
        pass

    @abstractmethod
    def get_policy(self, policy_id: str) -> Policy:
        """Retrieve a specific policy by ID."""
        pass

    @abstractmethod
    def clear_cache(self) -> None:
        """Clear any internal cache."""
        pass

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def validate(self) -> None:
        pass

    def health(self) -> bool:
        return True
