# kernel/managers/tests/test_repository_manager.py
import pytest
from unittest.mock import Mock

from kernel.managers import RepositoryManager
from kernel.lifecycle import Lifecycle, HealthStatus


class DummyRepository(Lifecycle):
    def _on_health(self) -> HealthStatus:
        return HealthStatus.HEALTHY


class TestRepositoryManager:
    def test_register_get(self):
        mgr = RepositoryManager()
        repo = DummyRepository()
        mgr.register("test", repo)
        assert mgr.has("test") is True
        assert mgr.get("test") == repo

    def test_register_duplicate(self):
        mgr = RepositoryManager()
        repo1 = DummyRepository()
        repo2 = DummyRepository()
        mgr.register("test", repo1)
        with pytest.raises(Exception, match="already registered"):
            mgr.register("test", repo2)

    def test_list(self):
        mgr = RepositoryManager()
        repo1 = DummyRepository()
        repo2 = DummyRepository()
        mgr.register("repo1", repo1)
        mgr.register("repo2", repo2)
        assert sorted(mgr.list()) == ["repo1", "repo2"]

    def test_health_all(self):
        mgr = RepositoryManager()
        repo = DummyRepository()
        mgr.register("test", repo)
        health = mgr.health_all()
        assert health["test"] == HealthStatus.HEALTHY
