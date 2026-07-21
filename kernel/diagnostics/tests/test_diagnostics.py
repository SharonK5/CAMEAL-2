# kernel/diagnostics/tests/test_diagnostics.py
import pytest
from unittest.mock import Mock
from kernel.diagnostics import Diagnostics, DiagnosticsRegistry
from kernel.diagnostics.lifecycle import DiagnosticsLifecycle
from kernel.events.event import Event
from kernel.lifecycle import HealthStatus


class TestDiagnostics:
    @pytest.fixture
    def diagnostics(self):
        return Diagnostics()

    def test_start_stop(self, diagnostics):
        assert diagnostics.running is False
        diagnostics.start()
        assert diagnostics.running is True
        diagnostics.stop()
        assert diagnostics.running is False

    def test_health(self):
        diag = Diagnostics()
        diag.register_health_check("test", lambda: HealthStatus.HEALTHY)
        health = diag.health()
        assert "test" in health
        assert health["test"] == HealthStatus.HEALTHY

    def test_metrics(self):
        diag = Diagnostics()
        diag.register_metric_provider("cpu", lambda: {"usage": 0.5})
        metrics = diag.metrics()
        assert "cpu" in metrics
        assert metrics["cpu"]["usage"] == 0.5

    def test_traces(self):
        diag = Diagnostics(trace_limit=2)
        diag.start()
        diag.record_event(Event(event_type="workflow.started"))
        diag.record_event(Event(event_type="workflow.started"))
        diag.record_event(Event(event_type="workflow.started"))
        traces = diag.traces()
        assert len(traces) == 2
        diag.stop()

    def test_logs(self):
        diag = Diagnostics(log_limit=3)
        diag.start()
        for i in range(5):
            diag.record_event(Event(event_type="log.info", payload={"id": i}))
        logs = diag.logs()
        assert len(logs) == 3
        diag.stop()

    def test_logs_filter(self):
        diag = Diagnostics()
        diag.start()
        diag.record_event(Event(event_type="log.info", payload={"msg": "info"}))
        diag.record_event(Event(event_type="log.error", payload={"msg": "error"}))
        logs = diag.logs(level="info")
        assert len(logs) == 1
        # level is derived from type
        assert logs[0]["type"] == "log.info"
        diag.stop()

    def test_registry_integration(self):
        registry = DiagnosticsRegistry()
        registry.register_health_check("custom", lambda: HealthStatus.HEALTHY)
        registry.register_metric_provider("custom_metric", lambda: 42)
        registry.register_trace_provider("custom_trace", lambda: [{"id": "trace1"}])
        registry.register_log_provider("custom_log", lambda: [{"msg": "log"}])

        diag = Diagnostics(registry=registry)
        diag.start()

        health = diag.health()
        assert "custom" in health
        metrics = diag.metrics()
        assert "custom_metric" in metrics
        traces = diag.traces()
        assert len(traces) >= 1
        logs = diag.logs()
        assert len(logs) >= 1

        diag.stop()

    def test_clear(self):
        diag = Diagnostics()
        diag.start()
        diag.record_event(Event(event_type="log.info"))
        assert len(diag.logs()) == 1
        diag.clear()
        assert len(diag.logs()) == 0
        diag.stop()

    def test_lifecycle(self):
        diag = Diagnostics()
        lifecycle = DiagnosticsLifecycle(diag)
        assert lifecycle.health() == HealthStatus.UNHEALTHY
        lifecycle.start()
        assert lifecycle.health() == HealthStatus.HEALTHY
        lifecycle.stop()
        assert lifecycle.health() == HealthStatus.UNHEALTHY

    def test_set_telemetry(self):
        diag = Diagnostics()
        telemetry = Mock()
        diag.set_telemetry_provider(telemetry)
        assert diag._telemetry is telemetry
