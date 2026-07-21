# kernel/diagnostics/registry/diagnostics_registry.py
"""
Registry for diagnostics components.

Allows components to register custom health checks, metric providers,
trace providers, and log providers.
"""

from typing import Dict, Callable, Any, List
from threading import RLock

from ...lifecycle import HealthStatus


class DiagnosticsRegistry:
    """
    Thread-safe registry for diagnostics providers.

    This registry holds callables that are invoked by the Diagnostics
    subsystem to collect health, metrics, traces, and logs.
    """

    def __init__(self) -> None:
        self._health_checks: Dict[str, Callable[[], HealthStatus]] = {}
        self._metric_providers: Dict[str, Callable[[], Any]] = {}
        self._trace_providers: Dict[str, Callable[[], List[Dict[str, Any]]]] = {}
        self._log_providers: Dict[str, Callable[[], List[Dict[str, Any]]]] = {}
        self._lock = RLock()

    # ---------- Health Checks ----------

    def register_health_check(self, name: str, check: Callable[[], HealthStatus]) -> None:
        """
        Register a health check function.

        Args:
            name: Unique name for the health check.
            check: Callable that returns a HealthStatus.
        """
        with self._lock:
            self._health_checks[name] = check

    def get_health_checks(self) -> Dict[str, Callable[[], HealthStatus]]:
        """Return all registered health checks."""
        with self._lock:
            return dict(self._health_checks)

    # ---------- Metric Providers ----------

    def register_metric_provider(self, name: str, provider: Callable[[], Any]) -> None:
        """
        Register a metric provider function.

        Args:
            name: Unique name for the metric.
            provider: Callable that returns a metric snapshot (dict or value).
        """
        with self._lock:
            self._metric_providers[name] = provider

    def get_metric_providers(self) -> Dict[str, Callable[[], Any]]:
        """Return all registered metric providers."""
        with self._lock:
            return dict(self._metric_providers)

    # ---------- Trace Providers ----------

    def register_trace_provider(self, name: str, provider: Callable[[], List[Dict[str, Any]]]) -> None:
        """
        Register a trace provider function.

        Args:
            name: Unique name for the trace source.
            provider: Callable that returns a list of trace dicts.
        """
        with self._lock:
            self._trace_providers[name] = provider

    def get_trace_providers(self) -> Dict[str, Callable[[], List[Dict[str, Any]]]]:
        """Return all registered trace providers."""
        with self._lock:
            return dict(self._trace_providers)

    # ---------- Log Providers ----------

    def register_log_provider(self, name: str, provider: Callable[[], List[Dict[str, Any]]]) -> None:
        """
        Register a log provider function.

        Args:
            name: Unique name for the log source.
            provider: Callable that returns a list of log dicts.
        """
        with self._lock:
            self._log_providers[name] = provider

    def get_log_providers(self) -> Dict[str, Callable[[], List[Dict[str, Any]]]]:
        """Return all registered log providers."""
        with self._lock:
            return dict(self._log_providers)

    # ---------- Utility ----------

    def clear(self) -> None:
        """Remove all registered providers (primarily for testing)."""
        with self._lock:
            self._health_checks.clear()
            self._metric_providers.clear()
            self._trace_providers.clear()
            self._log_providers.clear()

    def __len__(self) -> int:
        with self._lock:
            return (
                len(self._health_checks)
                + len(self._metric_providers)
                + len(self._trace_providers)
                + len(self._log_providers)
            )
