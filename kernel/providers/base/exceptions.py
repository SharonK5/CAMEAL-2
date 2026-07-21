# kernel/providers/base/exceptions.py
"""
Provider-specific exceptions.
"""


class ProviderError(Exception):
    """Base exception for all provider-related errors."""
    pass


class ProviderNotFoundError(ProviderError):
    """Raised when a requested provider is not registered in the registry."""
    pass


class ProviderRegistrationError(ProviderError):
    """Raised when attempting to register a provider with a name that is already taken."""
    pass


class ProviderInitializationError(ProviderError):
    """Raised when a provider fails during initialization (e.g., `start()`)."""
    pass


class ProviderConfigurationError(ProviderError):
    """
    Raised when provider configuration is invalid.

    Examples:
        - Missing required configuration keys
        - Invalid values (e.g., malformed URL, unsupported options)
        - Incompatible settings (e.g., conflicting parameters)
    """
    pass


class ProviderHealthError(ProviderError):
    """
    Raised when a provider's health check fails, but the provider itself may still be operational.

    This can be used to signal that the provider is unhealthy but not in a fatal state,
    allowing the kernel to take corrective action (e.g., retry, fallback).
    """
    pass
