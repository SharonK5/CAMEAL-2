# kernel/container/tests/test_container.py
import pytest
from abc import ABC, abstractmethod

from ..container import Container
from ..scopes import Scope
from ..exceptions import RegistrationError, ResolutionError, CircularDependencyError, StateError
from ..state import ContainerState
from .conftest import Repository, SQLRepository, MemoryRepository, Service, Logger, FileLogger, ConsoleLogger


class MissingInterface(ABC):
    @abstractmethod
    def do_something(self):
        pass


class A:
    def __init__(self, b: "B"): pass


class B:
    def __init__(self, a: A): pass


# ... rest of tests unchanged
