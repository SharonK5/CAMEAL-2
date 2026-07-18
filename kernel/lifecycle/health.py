# kernel/lifecycle/health.py
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from .states import LifecycleState


class HealthStatus(str, Enum):
    """Health status of a component."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class HealthReport:
    """
    Detailed health report for a component.
    """

    component: str
    state: LifecycleState
    healthy: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    uptime: Optional[float] = None
    version: Optional[str] = None
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def status(self) -> HealthStatus:
        if self.healthy:
            return HealthStatus.HEALTHY
        return HealthStatus.UNHEALTHY

    def to_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "state": self.state.value,
            "healthy": self.healthy,
            "timestamp": self.timestamp.isoformat(),
            "uptime": self.uptime,
            "version": self.version,
            "message": self.message,
            "details": self.details,
        }
