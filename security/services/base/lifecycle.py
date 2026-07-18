# security/services/base/lifecycle.py
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto


class ServiceState(Enum):
    """Rich lifecycle state for enterprise-grade service management."""

    CREATED = auto()
    INITIALIZING = auto()
    INITIALIZED = auto()
    VALIDATING = auto()
    VALIDATED = auto()
    STARTING = auto()
    RUNNING = auto()
    STOPPING = auto()
    STOPPED = auto()
    FAILED = auto()
    DISPOSED = auto()


class HealthStatus(Enum):
    """Health status for service monitoring."""

    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


class Lifecycle(ABC):
    """Standard lifecycle contract for all framework services."""

    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def validate(self) -> None: ...

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def health(self) -> HealthStatus: ...

    @abstractmethod
    def shutdown(self) -> None: ...

    @abstractmethod
    def dispose(self) -> None: ...
