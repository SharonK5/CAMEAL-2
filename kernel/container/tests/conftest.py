# kernel/container/tests/conftest.py
import pytest

from ..container import Container
from ..scopes import Scope


class Repository:
    pass


class SQLRepository(Repository):
    pass


class MemoryRepository(Repository):
    pass


class Service:
    def __init__(self, repo: Repository):
        self.repo = repo


class Logger:
    pass


class FileLogger(Logger):
    pass


class ConsoleLogger(Logger):
    pass


@pytest.fixture
def container():
    return Container()


@pytest.fixture
def container_with_registrations(container):
    container.register(Repository, SQLRepository, Scope.SINGLETON)
    container.register(Service, Service, Scope.REQUEST)
    container.register(Logger, FileLogger, Scope.TRANSIENT)
    return container
