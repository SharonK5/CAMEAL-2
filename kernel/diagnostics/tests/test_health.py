# kernel/diagnostics/tests/test_health.py
import pytest

from kernel.diagnostics.base.health_checker import HealthChecker
from kernel.lifecycle import HealthStatus


class TestHealthChecker:
    def test_register_and_check(self):
        checker = HealthChecker()
        checker.register("test", lambda: HealthStatus.HEALTHY)
        result = checker.check_all()
        assert result["test"] == HealthStatus.HEALTHY

    def test_check_failure(self):
        checker = HealthChecker()
        checker.register("failing", lambda: 1/0)  # Raises exception
        result = checker.check_all()
        assert result["failing"] == HealthStatus.UNHEALTHY

    def test_is_healthy_true(self):
        checker = HealthChecker()
        checker.register("a", lambda: HealthStatus.HEALTHY)
        checker.register("b", lambda: HealthStatus.HEALTHY)
        assert checker.is_healthy() is True

    def test_is_healthy_false(self):
        checker = HealthChecker()
        checker.register("a", lambda: HealthStatus.HEALTHY)
        checker.register("b", lambda: HealthStatus.UNHEALTHY)
        assert checker.is_healthy() is False
