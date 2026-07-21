# kernel/managers/__init__.py
"""
CAMEAL Kernel Managers.

Runtime orchestration components for the CAMEAL Kernel.

Provides:
- EngineManager: Coordinates cognitive engines.
- RepositoryManager: Manages domain repositories.
- WorkflowManager: Selects and executes workflows.
- ContextManager: Builds and propagates execution context.
- PluginManager: Manages plugin discovery and loading.
- SchedulerManager: Manages scheduled tasks.
"""

from .engine_manager import EngineManager
from .repository_manager import RepositoryManager
from .workflow_manager import WorkflowManager
from .context_manager import ContextManager
from .plugin_manager import PluginManager
from .scheduler_manager import SchedulerManager

from .exceptions import (
    ManagerError,
    ManagerRegistrationError,
    ManagerResolutionError,
    ManagerValidationError,
    ManagerLifecycleError,
    ManagerNotFoundError,
)

from .version import (
    __version__,
    __api_version__,
    VERSION,
    API_VERSION,
    API_STATUS,
    PACKAGE_NAME,
    DESCRIPTION,
    MIN_KERNEL_VERSION,
    MAX_KERNEL_VERSION,
    AUTHOR,
    LICENSE,
)

__all__ = [
    "EngineManager",
    "RepositoryManager",
    "WorkflowManager",
    "ContextManager",
    "PluginManager",
    "SchedulerManager",
    "ManagerError",
    "ManagerRegistrationError",
    "ManagerResolutionError",
    "ManagerValidationError",
    "ManagerLifecycleError",
    "ManagerNotFoundError",
    "__version__",
    "__api_version__",
    "VERSION",
    "API_VERSION",
    "API_STATUS",
    "PACKAGE_NAME",
    "DESCRIPTION",
    "MIN_KERNEL_VERSION",
    "MAX_KERNEL_VERSION",
    "AUTHOR",
    "LICENSE",
]
