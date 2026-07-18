# kernel/lifecycle/states.py
from enum import Enum


class LifecycleState(str, Enum):
    """
    Valid lifecycle states for a kernel-managed component.

    States progress in this order:
        CREATED → INITIALIZED → VALIDATED → BOOTED → STARTED → RUNNING
        RUNNING ↔ PAUSED
        RUNNING → STOPPING → STOPPED → SHUTDOWN → DISPOSED
        Any state → FAILED (terminal)
    """

    CREATED = "created"
    INITIALIZED = "initialized"
    VALIDATED = "validated"
    BOOTED = "booted"
    STARTED = "started"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    SHUTDOWN = "shutdown"
    DISPOSED = "disposed"
    FAILED = "failed"

    def __str__(self) -> str:
        return self.value
