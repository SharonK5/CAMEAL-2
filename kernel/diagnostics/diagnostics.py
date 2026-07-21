# kernel/diagnostics/diagnostics.py
import logging
from typing import Dict, Any, Optional, List

from ..lifecycle import HealthStatus

from .registry import DiagnosticsRegistry
from .base import HealthChecker, MetricsCollector, Tracer, Logger

try:
    from ..providers.telemetry import TelemetryProvider
except ImportError:
    TelemetryProvider = None  # type: ignore

logger = logging.getLogger(__name__)


class Diagnostics:
    def __init__(
        self,
        telemetry_provider: Optional[Any] = None,
        registry: Optional[DiagnosticsRegistry] = None,
        trace_limit: int = 100,
        log_limit: int = 500,
    ) -> None:
        self._telemetry = telemetry_provider
        self._registry = registry or DiagnosticsRegistry()

        # Core components
        self._health_checker = HealthChecker()
        self._metrics_collector = MetricsCollector()
        self._tracer = Tracer(trace_limit)
        self._logger = Logger(log_limit)

        self._running = False

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        logger.info("Diagnostics started")

    def stop(self) -> None:
        if not self._running:
            return
        self._running = False
        logger.info("Diagnostics stopped")

    @property
    def running(self) -> bool:
        return self._running

    # ---------- Public recording ----------
    def record_event(self, event) -> None:
        """Record an event for tracing and logging."""
        if not self._running:
            return
        self._tracer.record(event)
        self._logger.record(event)

    # ---------- Health ----------
    def health(self) -> Dict[str, HealthStatus]:
        result = {}
        for name, check in self._registry.get_health_checks().items():
            try:
                result[name] = check()
            except Exception as e:
                logger.error(f"Health check '{name}' failed: {e}")
                result[name] = HealthStatus.UNHEALTHY
        builtin = self._health_checker.check_all()
        result.update(builtin)
        return result

    def register_health_check(self, name: str, check: callable) -> None:
        self._health_checker.register(name, check)

    # ---------- Metrics ----------
    def metrics(self) -> Dict[str, Any]:
        result = {}
        for name, provider in self._registry.get_metric_providers().items():
            try:
                result[name] = provider()
            except Exception as e:
                logger.error(f"Metric provider '{name}' failed: {e}")
                result[name] = None
        builtin = self._metrics_collector.collect()
        result.update(builtin)
        return result

    def register_metric_provider(self, name: str, provider: callable) -> None:
        self._metrics_collector.register(name, provider)

    # ---------- Traces ----------
    def traces(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        traces = self._tracer.get_traces(limit)
        for name, provider in self._registry.get_trace_providers().items():
            try:
                extra = provider()
                if extra:
                    traces.extend(extra)
            except Exception as e:
                logger.error(f"Trace provider '{name}' failed: {e}")
        return traces

    def register_trace_provider(self, name: str, provider: callable) -> None:
        self._registry.register_trace_provider(name, provider)

    # ---------- Logs ----------
    def logs(self, limit: Optional[int] = None, level: Optional[str] = None) -> List[Dict[str, Any]]:
        logs = self._logger.get_logs(limit, level)
        for name, provider in self._registry.get_log_providers().items():
            try:
                extra = provider()
                if extra:
                    logs.extend(extra)
            except Exception as e:
                logger.error(f"Log provider '{name}' failed: {e}")
        return logs

    def register_log_provider(self, name: str, provider: callable) -> None:
        self._registry.register_log_provider(name, provider)

    # ---------- Telemetry ----------
    def set_telemetry_provider(self, telemetry_provider: Any) -> None:
        self._telemetry = telemetry_provider

    def clear(self) -> None:
        self._tracer.clear()
        self._logger.clear()
