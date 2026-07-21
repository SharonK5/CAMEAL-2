# kernel/bootstrap/exceptions.py
"""
Bootstrap-specific exceptions.
"""


class BootstrapError(Exception):
    """Base exception for all bootstrap-related errors."""


class ConfigurationError(BootstrapError):
    """Raised when configuration loading fails."""


class DiscoveryError(BootstrapError):
    """Raised when plugin discovery fails."""


class LoaderError(BootstrapError):
    """Raised when module loading fails."""


class ValidationError(BootstrapError):
    """Raised when runtime validation fails."""


class RegistrationError(BootstrapError):
    """Raised when component registration fails."""


class DependencyError(BootstrapError):
    """Raised when dependency resolution fails."""


class InitializationError(BootstrapError):
    """Raised when initialization fails."""
