# kernel/providers/base/interface.py
"""
Additional interfaces for specialized providers.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class ProviderInterface(ABC):
    """
    Base marker interface for provider contracts.

    All providers implicitly implement this via the `Provider` base class.
    This exists for explicit typing and future extension.
    """
    pass


class ConfigurableProvider(ABC):
    """
    Providers that accept runtime configuration.

    Useful for:
        - Updating API keys or credentials at runtime
        - Changing endpoint URLs
        - Adjusting timeouts or retry settings
    """

    @abstractmethod
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Apply configuration to the provider.

        Args:
            config: Configuration dictionary (keys depend on provider).

        Raises:
            ProviderConfigurationError: If configuration is invalid.
        """
        pass


class HealthCheckProvider(ABC):
    """
    Providers with detailed health information beyond a simple boolean status.

    Useful for monitoring systems that need granular health data,
    such as latency percentiles, error rates, or dependency status.
    """

    @abstractmethod
    def health_details(self) -> Dict[str, Any]:
        """
        Return detailed health information.

        Returns:
            A dictionary containing:
                - status: "healthy", "degraded", or "unhealthy"
                - timestamp: ISO format timestamp
                - details: provider-specific information (e.g., latency, error rates)
        """
        pass


class ResettableProvider(ABC):
    """
    Providers that can be reset to a clean state.

    Useful for:
        - Clearing caches
        - Resetting connections
        - Clearing temporary state during testing
        - Re-initializing after configuration changes
    """

    @abstractmethod
    def reset(self) -> None:
        """Reset the provider to its initial (or clean) state."""
        pass
