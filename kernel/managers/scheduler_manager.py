# kernel/managers/scheduler_manager.py
"""
Scheduler Manager – manages scheduled tasks.
"""

from typing import Any, Callable, Dict, List, Optional
from ..lifecycle import Lifecycle, HealthStatus
from .manager import Manager
from .exceptions import ManagerValidationError


class SchedulerManager(Manager):
    """
    Manages scheduled tasks.

    Responsibilities:
        - Register scheduled tasks.
        - Start and stop the scheduler.
        - Execute tasks on schedule.
    """

    def __init__(self) -> None:
        super().__init__("scheduler_manager")
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._running = False

    def register(self, name: str, interval: float, target: Callable, **kwargs) -> None:
        """Register a scheduled task."""
        self._validator.validate_name(name)
        if not callable(target):
            raise ManagerValidationError("Target must be callable")
        if interval <= 0:
            raise ManagerValidationError("Interval must be positive")
        self._tasks[name] = {"interval": interval, "target": target, "args": kwargs}

    def start_all(self) -> None:
        """Start the scheduler."""
        self._running = True
        # In a real implementation, this would start a background thread or asyncio loop.

    def stop_all(self) -> None:
        """Stop the scheduler."""
        self._running = False

    def health_all(self) -> Dict[str, HealthStatus]:
        """Return health status of the scheduler."""
        return {"scheduler": HealthStatus.HEALTHY if self._running else HealthStatus.UNHEALTHY}

    def __len__(self) -> int:
        return len(self._tasks)
