# kernel/diagnostics/collectors/kernel_collector.py
"""
Collector for kernel-level diagnostics.
"""

import logging
from typing import Dict, Any, List

from ...lifecycle import HealthStatus
from ..registry.diagnostics_registry import DiagnosticsRegistry

logger = logging.getLogger(__name__)


class KernelCollector:
    """
    Collects diagnostics from the kernel itself (lifecycle, container, etc.).
    """

    def __init__(self, registry: DiagnosticsRegistry):
        self._registry = registry
        self._register()

    def _register(self) -> None:
        """Register health checks and metric providers."""
        self._registry.register_health_check("kernel", self._health_check)
        self._registry.register_metric_provider("kernel_metrics", self._collect_metrics)
        self._registry.register_trace_provider("kernel_traces", self._collect_traces)
        self._registry.register_log_provider("kernel_logs", self._collect_logs)

    def _health_check(self) -> HealthStatus:
        return HealthStatus.HEALTHY

    def _collect_metrics(self) -> Dict[str, Any]:
        return {
            "components_registered": len(self._registry.get_health_checks()),
            "providers_registered": len(self._registry.get_metric_providers()),
        }

    def _collect_traces(self) -> List[Dict[str, Any]]:
        return []

    def _collect_logs(self) -> List[Dict[str, Any]]:
        return []
