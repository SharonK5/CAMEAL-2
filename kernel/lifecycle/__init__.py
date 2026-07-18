# kernel/lifecycle/__init__.py
"""
CAMEAL Kernel Lifecycle.

Defines the standard lifecycle contract for all kernel-managed components.

Provides:
- Lifecycle interface
- Pausable (optional)
- LifecycleManager for orchestration
- LifecycleState enumeration
- HealthStatus and HealthReport
- LifecycleObserver for event notification
- Diagnostics aggregation
- LifecycleError for invalid transitions
"""

from .lifecycle import Lifecycle, Pausable
from .manager import LifecycleManager
from .states import LifecycleState
from .health import HealthStatus, HealthReport
from .observer import LifecycleObserver, NullObserver
from .diagnostics import Diagnostics
from .exceptions import LifecycleError
from .version import __version__, __api_version__, VERSION, API_STATUS, PACKAGE_NAME, DESCRIPTION

__all__ = [
    "Lifecycle",
    "Pausable",
    "LifecycleManager",
    "LifecycleState",
    "HealthStatus",
    "HealthReport",
    "LifecycleObserver",
    "NullObserver",
    "Diagnostics",
    "LifecycleError",
    "__version__",
    "__api_version__",
    "VERSION",
    "API_STATUS",
    "PACKAGE_NAME",
    "DESCRIPTION",
]
