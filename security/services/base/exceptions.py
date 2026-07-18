"""
exceptions.py

Exception hierarchy for the Security Services Framework.

These exceptions are intentionally independent of any specific security
domain (authentication, authorization, policy, etc.) and represent
framework-level failures.
"""

from __future__ import annotations


class SecurityServiceError(Exception):
    """Base exception for all Security Service framework errors."""


class ServiceConfigurationError(SecurityServiceError):
    """Raised when a service has an invalid configuration."""


class ServiceRegistrationError(SecurityServiceError):
    """Raised when service registration fails."""


class ServiceResolutionError(SecurityServiceError):
    """Raised when a requested service cannot be resolved."""


class ServiceValidationError(SecurityServiceError):
    """Raised when validation fails."""


class ServiceInitializationError(SecurityServiceError):
    """Raised when initialization fails."""


class ServiceShutdownError(SecurityServiceError):
    """Raised when shutdown fails."""


class ServiceLifecycleError(SecurityServiceError):
    """Raised when an invalid lifecycle transition occurs."""


class ServiceHealthError(SecurityServiceError):
    """Raised when a service health check fails."""
