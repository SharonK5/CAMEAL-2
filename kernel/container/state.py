# kernel/container/state.py
from enum import Enum


class ContainerState(str, Enum):
    """Valid states for the container lifecycle."""

    CREATED = "created"
    DISCOVERED = "discovered"
    VALIDATED = "validated"
    INITIALIZED = "initialized"
    FROZEN = "frozen"
    RUNNING = "running"
    STOPPED = "stopped"
    DISPOSED = "disposed"
    FAILED = "failed"

    def __str__(self) -> str:
        return self.value
