# kernel/__init__.py
"""
CAMEAL Kernel Runtime.

The CAMEAL Kernel is the runtime entry point of the CAMEAL platform.
"""

from .kernel import Kernel
from .models import Request, Response

from .exceptions import (
    KernelError,
    ConfigurationError,
    ValidationError,
    DependencyError,
    PluginError,
    ExecutionError,
    LifecycleError,
    ComponentNotFoundError,
    RegistrationError,
    WorkflowError,
    ContextError,
    SchedulerError,
    EventError,
)

# Bootstrap is imported separately when needed
# from .bootstrap import Bootstrap  # <-- remove or comment out

__version__ = "1.0.0"

__all__ = [
    "Kernel",
    "Request",
    "Response",
    # "Bootstrap",  # <-- remove if not needed at top level
    "KernelError",
    "ConfigurationError",
    "ValidationError",
    "DependencyError",
    "PluginError",
    "ExecutionError",
    "LifecycleError",
    "ComponentNotFoundError",
    "RegistrationError",
    "WorkflowError",
    "ContextError",
    "SchedulerError",
    "EventError",
]
