# kernel/diagnostics/tests/test_registry.py
import pytest
from kernel.diagnostics.registry import DiagnosticsRegistry
from kernel.lifecycle import HealthStatus


class TestDiagnosticsRegistry:
    def test_register_health_check(self):
        registry = DiagnosticsRegistry()
        registry.register_health_check("test", lambda: HealthStatus.HEALTHY)
        checks = registry.get_health_checks()
        assert "test" in checks
        assert checks["test"]() == HealthStatus.HEALTHY

    def test_register_metric_provider(self):
        registry = DiagnosticsRegistry()
        registry.register_metric_provider("cpu", lambda: 42)
        providers = registry.get_metric_providers()
        assert "cpu" in providers
        assert providers["cpu"]() == 42

    def test_register_trace_provider(self):
        registry = DiagnosticsRegistry()
        registry.register_trace_provider("traces", lambda: [{"id": 1}])
        providers = registry.get_trace_providers()
        assert "traces" in providers
        assert providers["traces"]() == [{"id": 1}]

    def test_register_log_provider(self):
        registry = DiagnosticsRegistry()
        registry.register_log_provider("logs", lambda: [{"msg": "test"}])
        providers = registry.get_log_providers()
        assert "logs" in providers
        assert providers["logs"]() == [{"msg": "test"}]

    def test_clear(self):
        registry = DiagnosticsRegistry()
        registry.register_health_check("test", lambda: HealthStatus.HEALTHY)
        assert len(registry) > 0
        registry.clear()
        assert len(registry) == 0
