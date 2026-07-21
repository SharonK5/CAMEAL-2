# kernel/providers/base/__init__.py
"""
Provider base abstractions.

This package contains the core contracts that all providers must implement.
"""

from .provider import Provider
from .interface import (
    ProviderInterface,
    ConfigurableProvider,
    HealthCheckProvider,
    ResettableProvider,
)
from .exceptions import (
    ProviderError,
    ProviderNotFoundError,
    ProviderRegistrationError,
    ProviderInitializationError,
    ProviderConfigurationError,
    ProviderHealthError,
)

__all__ = [
    # Core
    "Provider",
    "ProviderInterface",
    # Optional interfaces
    "ConfigurableProvider",
    "HealthCheckProvider",
    "ResettableProvider",
    # Exceptions
    "ProviderError",
    "ProviderNotFoundError",
    "ProviderRegistrationError",
    "ProviderInitializationError",
    "ProviderConfigurationError",
    "ProviderHealthError",
]
