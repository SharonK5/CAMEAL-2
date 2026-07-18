# kernel/lifecycle.py
"""
CAMEAL Kernel Lifecycle (stub).

Minimal stub required for container tests.
The full lifecycle implementation will be added later.
"""

from enum import Enum


class LifecycleState(str, Enum):
    CREATED = "created"
    DISCOVERED = "discovered"
    VALIDATED = "validated"
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    DISPOSED = "disposed"
    FAILED = "failed"


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class Lifecycle:
    """Minimal lifecycle stub for container tests."""

    def __init__(self) -> None:
        self._state = LifecycleState.CREATED

    @property
    def state(self) -> LifecycleState:
        return self._state

    def discover(self) -> None:
        self._state = LifecycleState.DISCOVERED

    def validate(self) -> None:
        self._state = LifecycleState.VALIDATED

    def initialize(self) -> None:
        self._state = LifecycleState.INITIALIZED

    def start(self) -> None:
        self._state = LifecycleState.RUNNING

    def pause(self) -> None:
        self._state = LifecycleState.PAUSED

    def resume(self) -> None:
        self._state = LifecycleState.RUNNING

    def stop(self) -> None:
        self._state = LifecycleState.STOPPED

    def shutdown(self) -> None:
        self._state = LifecycleState.STOPPED

    def dispose(self) -> None:
        self._state = LifecycleState.DISPOSED

    def health(self) -> HealthStatus:
        return HealthStatus.HEALTHY
