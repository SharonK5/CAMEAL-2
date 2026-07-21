# kernel/managers/exceptions.py
"""
Manager-specific exceptions.
"""


class ManagerError(Exception):
    """Base exception for all manager-related errors."""


class ManagerRegistrationError(ManagerError):
    """Raised when manager registration fails."""


class ManagerResolutionError(ManagerError):
    """Raised when manager resolution fails."""


class ManagerValidationError(ManagerError):
    """Raised when manager validation fails."""


class ManagerLifecycleError(ManagerError):
    """Raised when manager lifecycle operations fail."""


class ManagerNotFoundError(ManagerError):
    """Raised when a manager is not found."""
