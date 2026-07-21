# kernel/managers/tests/test_engine_manager.py
import pytest
from unittest.mock import Mock

from kernel.managers import EngineManager
from kernel.managers.exceptions import ManagerRegistrationError, ManagerResolutionError
from kernel.lifecycle import Lifecycle, HealthStatus


class DummyEngine(Lifecycle):
    def __init__(self, name: str = "dummy"):
        super().__init__()
        self._name = name

    def _on_health(self) -> HealthStatus:
        return HealthStatus.HEALTHY


class TestEngineManager:
    def test_register_get(self):
        mgr = EngineManager()
        engine = DummyEngine()
        mgr.register("test", engine, ["read"])
        assert mgr.has("test") is True
        assert mgr.get("test") == engine

    def test_register_duplicate(self):
        mgr = EngineManager()
        engine1 = DummyEngine()
        engine2 = DummyEngine()
        mgr.register("test", engine1, ["read"])
        with pytest.raises(ManagerRegistrationError, match="already registered"):
            mgr.register("test", engine2, ["write"])

    def test_register_capability_conflict(self):
        mgr = EngineManager()
        engine1 = DummyEngine()
        engine2 = DummyEngine()
        mgr.register("engine1", engine1, ["read"])
        with pytest.raises(ManagerResolutionError, match="already registered"):
            mgr.register("engine2", engine2, ["read"])

    def test_get_by_capability(self):
        mgr = EngineManager()
        engine = DummyEngine()
        mgr.register("test", engine, ["read", "write"])
        assert mgr.get_by_capability("read") == engine
        assert mgr.has_capability("write") is True
        assert mgr.has_capability("delete") is False

    def test_list(self):
        mgr = EngineManager()
        engine1 = DummyEngine()
        engine2 = DummyEngine()
        mgr.register("engine1", engine1, [])
        mgr.register("engine2", engine2, [])
        assert sorted(mgr.list()) == ["engine1", "engine2"]

    def test_health_all(self):
        mgr = EngineManager()
        engine = DummyEngine()
        mgr.register("test", engine, [])
        health = mgr.health_all()
        assert health["test"] == HealthStatus.HEALTHY
