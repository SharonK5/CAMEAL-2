# kernel/container/tests/test_validator.py
import pytest
from abc import ABC, abstractmethod

from ..validator import Validator
from ..registry import Registry
from ..dependency import Dependency
from ..scopes import Scope
from ..exceptions import ValidationError, CircularDependencyError
from .conftest import Repository, SQLRepository


class A:
    def __init__(self, b: "B"): pass


class B:
    def __init__(self, a: A): pass


class MissingInterface(ABC):
    @abstractmethod
    def do_something(self):
        pass


class ServiceWithMissing:
    def __init__(self, missing: MissingInterface): pass


class TestValidator:
    def test_validate_valid_graph(self):
        registry = Registry()
        validator = Validator(registry)
        registry.register(Dependency(Repository, SQLRepository, Scope.SINGLETON))
        validator.validate_graph()

    def test_validate_missing_dependency(self):
        registry = Registry()
        validator = Validator(registry)
        registry.register(Dependency(ServiceWithMissing, ServiceWithMissing, Scope.TRANSIENT))
        with pytest.raises(ValidationError, match="Cannot resolve parameter"):
            validator.validate_graph()

    def test_validate_circular_dependency(self):
        registry = Registry()
        validator = Validator(registry)
        registry.register(Dependency(A, A, Scope.TRANSIENT))
        registry.register(Dependency(B, B, Scope.TRANSIENT))
        with pytest.raises(CircularDependencyError, match="Circular"):
            validator.validate_graph()

    def test_validate_registration_invalid_implementation(self):
        registry = Registry()
        validator = Validator(registry)
        dep = Dependency(Repository, 123, Scope.SINGLETON)  # type: ignore
        with pytest.raises(ValidationError, match="must be a class or callable"):
            validator.validate_registration(dep)
