# kernel/container/tests/test_registry.py
import pytest

from ..registry import Registry
from ..dependency import Dependency
from ..scopes import Scope
from ..exceptions import RegistrationError
from .conftest import Repository, SQLRepository, MemoryRepository, Logger, FileLogger, ConsoleLogger


class TestRegistry:
    def test_register_get(self):
        registry = Registry()
        dep = Dependency(Repository, SQLRepository, Scope.SINGLETON)
        registry.register(dep)
        result = registry.get(dep.identifier)
        assert result is dep

    def test_register_duplicate_raises(self):
        registry = Registry()
        dep1 = Dependency(Repository, SQLRepository, Scope.SINGLETON, name="sql")
        dep2 = Dependency(Repository, MemoryRepository, Scope.SINGLETON, name="sql")
        registry.register(dep1)
        with pytest.raises(RegistrationError, match="already registered"):
            registry.register(dep2)

    def test_get_by_interface(self):
        registry = Registry()
        dep1 = Dependency(Repository, SQLRepository, Scope.SINGLETON, name="sql")
        dep2 = Dependency(Repository, MemoryRepository, Scope.SINGLETON, name="memory")
        registry.register(dep1)
        registry.register(dep2)
        results = registry.get_by_interface(Repository)
        assert len(results) == 2
        assert dep1 in results
        assert dep2 in results

    def test_get_by_tag(self):
        registry = Registry()
        dep1 = Dependency(Logger, FileLogger, Scope.SINGLETON, name="file", tags=("file", "prod"))
        dep2 = Dependency(Logger, ConsoleLogger, Scope.SINGLETON, name="console", tags=("console", "dev"))
        registry.register(dep1)
        registry.register(dep2)
        results = registry.get_by_tag("file")
        assert len(results) == 1
        assert results[0] is dep1

    def test_freeze(self):
        registry = Registry()
        dep = Dependency(Repository, SQLRepository, Scope.SINGLETON)
        registry.register(dep)
        registry.freeze()
        with pytest.raises(RegistrationError, match="frozen"):
            registry.register(dep)

    def test_statistics(self):
        registry = Registry()
        dep1 = Dependency(Repository, SQLRepository, Scope.SINGLETON)
        dep2 = Dependency(Logger, FileLogger, Scope.SINGLETON)
        registry.register(dep1)
        registry.register(dep2)
        stats = registry.statistics()
        assert stats["registrations"] == 2
        assert stats["interfaces"] == 2
        assert stats["frozen"] is False
