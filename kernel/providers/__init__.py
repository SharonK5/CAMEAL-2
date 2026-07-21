# kernel/providers/__init__.py
"""
CAMEAL Kernel Providers.

Providers are infrastructure adapters that expose standardized capabilities
to engines, plugins, and workflows while abstracting external technologies.

Providers contain NO business decision logic. They are responsible only for
infrastructure interaction and capability exposure.
"""

from .base.provider import Provider
from .base.interface import (
    ProviderInterface,
    ConfigurableProvider,
    HealthCheckProvider,
    ResettableProvider,
)
from .base.exceptions import (
    ProviderError,
    ProviderNotFoundError,
    ProviderRegistrationError,
    ProviderInitializationError,
    ProviderConfigurationError,
)

from .registry.provider_registry import ProviderRegistry

from .lifecycle.provider_lifecycle import ProviderLifecycle

__all__ = [
    # Core
    "Provider",
    "ProviderInterface",
    "ProviderRegistry",
    "ProviderLifecycle",

    # Additional interfaces
    "ConfigurableProvider",
    "HealthCheckProvider",
    "ResettableProvider",

    # Exceptions
    "ProviderError",
    "ProviderNotFoundError",
    "ProviderRegistrationError",
    "ProviderInitializationError",
    "ProviderConfigurationError",
]
