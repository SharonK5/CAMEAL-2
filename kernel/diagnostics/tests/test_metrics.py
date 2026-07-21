# kernel/diagnostics/tests/test_metrics.py
import pytest

from kernel.diagnostics.base.metrics_collector import MetricsCollector


class TestMetricsCollector:
    def test_register_and_collect(self):
        collector = MetricsCollector()
        collector.register("cpu", lambda: 0.5)
        collector.register("memory", lambda: {"used": 1024})
        result = collector.collect()
        assert "timestamp" in result
        assert result["cpu"] == 0.5
        assert result["memory"] == {"used": 1024}

    def test_collect_error(self):
        collector = MetricsCollector()
        collector.register("failing", lambda: 1/0)
        result = collector.collect()
        assert result["failing"] is None

    def test_clear(self):
        collector = MetricsCollector()
        collector.register("a", lambda: 1)
        assert len(collector._providers) == 1
        collector.clear()
        assert len(collector._providers) == 0
