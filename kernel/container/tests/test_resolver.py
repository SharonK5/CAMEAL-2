# kernel/container/tests/test_resolver.py
import pytest

from ..resolver import Resolver
from ..registry import Registry
from ..cache import Cache
from ..validator import Validator
from ..dependency import Dependency
from ..scopes import Scope
from ..exceptions import ResolutionError, CircularDependencyError
from .conftest import Repository, SQLRepository, MemoryRepository, Service, Logger, FileLogger, ConsoleLogger


# Circular dependency classes
class A:
    def __init__(self, b: "B"): pass
class B:
    def __init__(self, a: A): pass


class TestResolver:
    # ... tests as before ...

    def test_resolve_circular_dependency(self):
        registry = Registry()
        cache = Cache()
        validator = Validator(registry)
        resolver = Resolver(registry, cache, validator)

        registry.register(Dependency(A, A, Scope.TRANSIENT))
        registry.register(Dependency(B, B, Scope.TRANSIENT))

        with pytest.raises(CircularDependencyError, match="Circular"):
            resolver.resolve(A)

    # ... rest of tests ...
