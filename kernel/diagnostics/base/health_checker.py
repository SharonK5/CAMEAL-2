# kernel/diagnostics/base/health_checker.py
"""
Health checker – aggregates health status from registered checks.
"""

from typing import Dict, Callable

from ...lifecycle import HealthStatus


class HealthChecker:
    """
    Aggregates health status from registered health check functions.
    """

    def __init__(self):
        self._checks: Dict[str, Callable[[], HealthStatus]] = {}

    def register(self, name: str, check: Callable[[], HealthStatus]) -> None:
        """
        Register a health check.

        Args:
            name: The name of the component being checked.
            check: A callable that returns a HealthStatus.
        """
        self._checks[name] = check

    def check_all(self) -> Dict[str, HealthStatus]:
        """
        Execute all registered health checks.

        Returns:
            A dictionary mapping component name to HealthStatus.
        """
        result = {}
        for name, check in self._checks.items():
            try:
                result[name] = check()
            except Exception:
                result[name] = HealthStatus.UNHEALTHY
        return result

    def is_healthy(self) -> bool:
        """
        Return True if all registered health checks return HEALTHY.
        """
        statuses = self.check_all()
        return all(s == HealthStatus.HEALTHY for s in statuses.values())
