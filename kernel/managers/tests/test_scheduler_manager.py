# kernel/managers/tests/test_scheduler_manager.py
import pytest

from kernel.managers import SchedulerManager
from kernel.managers.exceptions import ManagerValidationError


class TestSchedulerManager:
    def test_register(self):
        mgr = SchedulerManager()
        calls = []

        def task():
            calls.append("called")

        mgr.register("test", 1.0, task)
        assert len(mgr) == 1

    def test_register_invalid_interval(self):
        mgr = SchedulerManager()
        with pytest.raises(ManagerValidationError, match="positive"):
            mgr.register("test", 0, lambda: None)

    def test_register_invalid_target(self):
        mgr = SchedulerManager()
        with pytest.raises(ManagerValidationError, match="callable"):
            mgr.register("test", 1.0, "not callable")

    def test_health(self):
        mgr = SchedulerManager()
        health = mgr.health_all()
        assert "scheduler" in health
        assert health["scheduler"].value == "unhealthy"

        mgr.start_all()
        health = mgr.health_all()
        assert health["scheduler"].value == "healthy"
