# kernel/diagnostics/collectors/provider_collector.py
"""
Collector for provider diagnostics.
"""

import logging
from typing import Dict, Any

from ...providers import ProviderRegistry
from ...lifecycle import HealthStatus
from ..registry.diagnostics_registry import DiagnosticsRegistry

logger = logging.getLogger(__name__)


class ProviderCollector:
    """
    Collects diagnostics from providers.
    """

    def __init__(self, provider_registry: ProviderRegistry, registry: DiagnosticsRegistry):
        self._provider_registry = provider_registry
        self._registry = registry
        self._register()

    def _register(self) -> None:
        self._registry.register_health_check("providers", self._health_check)
        self._registry.register_metric_provider("provider_metrics", self._collect_metrics)

    def _health_check(self) -> HealthStatus:
        try:
            # Check if we can list providers
            _ = self._provider_registry.list()
            return HealthStatus.HEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY

    def _collect_metrics(self) -> Dict[str, Any]:
        providers = self._provider_registry.list()
        return {
            "total_providers": len(providers),
            "provider_names": providers,
        }
