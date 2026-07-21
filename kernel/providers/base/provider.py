# kernel/providers/base/provider.py
"""
Base provider abstract class.
"""

from abc import ABC, abstractmethod
from typing import Any

from ...lifecycle import Lifecycle, HealthStatus


class Provider(Lifecycle, ABC):
    """
    Base interface for all providers.

    Providers are infrastructure adapters that expose standardized
    capabilities to engines, plugins, and workflows while abstracting
    external technologies and services.

    Providers contain NO business decision logic. They are responsible
    only for infrastructure interaction and capability exposure.

    All providers must implement:
        - get() → return the underlying client or resource
        - start() → initialize connections (inherited from Lifecycle)
        - stop() → clean up resources (inherited from Lifecycle)
        - health() → report operational status (inherited from Lifecycle)

    The kernel depends on provider contracts, not specific implementations.
    """

    @abstractmethod
    def get(self) -> Any:
        """
        Return the underlying client or resource.

        This is the primary accessor for the provider's capability.

        Example:
            cache = cache_provider.get()   # returns a cache client
            llm = llm_provider.get()       # returns an LLM client
            storage = storage_provider.get() # returns a storage client
        """
        pass

    # ✅ FIX: implement abstract method _on_health from Lifecycle
    def _on_health(self) -> bool:
        """
        Default health check: delegates to the public health() method.
        """
        return self.health() == HealthStatus.HEALTHY

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name={getattr(self, 'name', 'unnamed')})>"
