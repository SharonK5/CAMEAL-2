"""
CAMEAL Kernel Package

The kernel is the orchestration layer of the CAMEAL platform.
It coordinates system components, manages workflows, routes requests,
and maintains the runtime state without implementing business logic.

Modules
-------
- cameal_kernel: Main kernel entry point.
- orchestrator: Coordinates workflows.
- router: Routes requests to registered services.
- registry: Service registration and discovery.
- state_manager: Runtime state management.
- event_bus: Event-based communication.
- lifecycle: Startup and shutdown management.
- version: Kernel version information.

Author:
    Sharon Rhodah Kaitano

License:
    MIT License
"""

from .version import __version__

__all__ = [
    "__version__",
]
