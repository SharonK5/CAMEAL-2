# kernel/exceptions.py
"""
CAMEAL Kernel Exceptions

Defines the exception hierarchy for the CAMEAL Kernel.

The kernel raises only exceptions derived from ``KernelError``.
Applications may either catch specific exceptions or catch
``KernelError`` to handle all kernel-related failures.
"""

from __future__ import annotations


class KernelError(Exception):
    """Base exception for all kernel-related errors."""


class ConfigurationError(KernelError):
    """Raised when kernel configuration is invalid or incomplete."""


class ValidationError(KernelError):
    """Raised when validation of a runtime object fails."""


class ExecutionError(KernelError):
    """Raised during workflow execution."""


class DependencyError(KernelError):
    """Raised when dependency registration or resolution fails."""


class PluginError(KernelError):
    """Raised during plugin discovery, loading, or validation."""


class LifecycleError(KernelError):
    """Raised when an invalid lifecycle transition occurs."""


class ComponentNotFoundError(KernelError):
    """Raised when a requested component cannot be found."""


class RegistrationError(KernelError):
    """Raised when attempting to register a duplicate component."""


class WorkflowError(KernelError):
    """Raised when workflow construction or execution fails."""


class ContextError(KernelError):
    """Raised when an execution context is invalid or inconsistent."""


class SchedulerError(KernelError):
    """Raised when scheduled jobs cannot be executed."""


class EventError(KernelError):
    """Raised when event publication or dispatch fails."""
