# kernel/providers/registry/provider_registry.py
"""
Thread-safe registry for providers.
"""

from typing import Dict, List, Optional, Iterator, Tuple
from threading import RLock

from ..base.provider import Provider
from ..base.exceptions import ProviderNotFoundError, ProviderRegistrationError


class ProviderRegistry:
    """
    Registry for all providers.

    Thread-safe. Providers are stored by unique name (string).

    The registry is the central authority for provider resolution.
    It is typically instantiated during kernel bootstrap and made
    available to engines and other components.

    Usage:
        registry = ProviderRegistry()
        registry.register("llm", OllamaProvider())
        llm = registry.get("llm")
    """

    def __init__(self) -> None:
        self._providers: Dict[str, Provider] = {}
        self._lock = RLock()

    def register(self, name: str, provider: Provider) -> None:
        """
        Register a provider.

        Args:
            name: Unique identifier for the provider.
            provider: The provider instance.

        Raises:
            ProviderRegistrationError: If a provider with the same name is already registered.
        """
        with self._lock:
            if name in self._providers:
                raise ProviderRegistrationError(
                    f"Provider '{name}' already registered"
                )
            self._providers[name] = provider

    def get(self, name: str) -> Provider:
        """
        Retrieve a provider by name.

        Args:
            name: Provider identifier.

        Returns:
            The provider instance.

        Raises:
            ProviderNotFoundError: If no provider is registered with that name.
        """
        with self._lock:
            if name not in self._providers:
                raise ProviderNotFoundError(f"Provider '{name}' not found")
            return self._providers[name]

    def has(self, name: str) -> bool:
        """
        Check if a provider is registered.

        Args:
            name: Provider identifier.

        Returns:
            True if the provider exists, False otherwise.
        """
        with self._lock:
            return name in self._providers

    def list(self) -> List[str]:
        """
        Return a list of all registered provider names.

        Returns:
            A list of provider names (sorted for deterministic ordering).
        """
        with self._lock:
            return sorted(self._providers.keys())

    def all(self) -> List[Provider]:
        """
        Return a list of all registered provider instances.

        Returns:
            A list of provider instances (in registration order).
        """
        with self._lock:
            return list(self._providers.values())

    def __len__(self) -> int:
        with self._lock:
            return len(self._providers)

    def __iter__(self) -> Iterator[Tuple[str, Provider]]:
        with self._lock:
            return iter(self._providers.items())

    def clear(self) -> None:
        """Clear all registered providers (primarily for testing)."""
        with self._lock:
            self._providers.clear()
