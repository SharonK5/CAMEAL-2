# kernel/diagnostics/base/metrics_collector.py
"""
Metrics collector – collects metrics from registered providers.
"""

from typing import Dict, Any, Callable
import time


class MetricsCollector:
    """
    Collects metrics from registered metric providers.
    """

    def __init__(self):
        self._providers: Dict[str, Callable[[], Any]] = {}

    def register(self, name: str, provider: Callable[[], Any]) -> None:
        """
        Register a metric provider.

        Args:
            name: The name of the metric.
            provider: A callable that returns a metric snapshot.
        """
        self._providers[name] = provider

    def collect(self) -> Dict[str, Any]:
        """
        Collect all registered metrics.

        Returns:
            A dictionary with a timestamp and each metric.
        """
        result = {"timestamp": time.time()}
        for name, provider in self._providers.items():
            try:
                result[name] = provider()
            except Exception:
                result[name] = None
        return result

    def clear(self) -> None:
        """Clear all registered providers."""
        self._providers.clear()
