"""
Custom exceptions used throughout the CAMEAL Kernel.
"""


class KernelError(Exception):
    """Base exception for all kernel-related errors."""


class ModuleRegistrationError(KernelError):
    """Raised when a module cannot be registered."""


class ModuleNotFoundError(KernelError):
    """Raised when a requested module is not registered."""


class RoutingError(KernelError):
    """Raised when a request cannot be routed."""


class WorkflowError(KernelError):
    """Raised when workflow execution fails."""


class LifecycleError(KernelError):
    """Raised during startup or shutdown failures."""
