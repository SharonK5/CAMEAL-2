"""
===============================================================================
Tests for repository.repository_manager
===============================================================================
"""

import pytest

from repository.repository import Repository
from repository.repository_factory import RepositoryFactory
from repository.repository_manager import RepositoryManager


class DummyRepository(Repository):

    @property
    def name(self):
        return "Dummy"

    @property
    def version(self):
        return "1.0"

    def contains(self, identifier):
        return False

    def get(self, identifier):
        raise KeyError(identifier)

    def list(self):
        return ()

    def search(self, query):
        return ()

    def register(self, asset):
        pass

    def unregister(self, identifier):
        pass

    def clear(self):
        pass

    def size(self):
        return 0


def build_repository():
    return DummyRepository()


def test_register():

    manager = RepositoryManager()

    manager.register(
        "repo",
        DummyRepository(),
    )

    assert manager.size() == 1


def test_unregister():

    manager = RepositoryManager()

    manager.register(
        "repo",
        DummyRepository(),
    )

    manager.unregister("repo")

    assert manager.size() == 0


def test_contains():

    manager = RepositoryManager()

    manager.register(
        "repo",
        DummyRepository(),
    )

    assert manager.contains("repo")


def test_get():

    manager = RepositoryManager()

    repository = DummyRepository()

    manager.register(
        "repo",
        repository,
    )

    assert manager.get("repo") is repository


def test_factory_creation():

    factory = RepositoryFactory()

    factory.register(
        "dummy",
        build_repository,
    )

    manager = RepositoryManager(
        factory=factory,
    )

    repository = manager.create(
        "repo",
        "dummy",
    )

    assert isinstance(
        repository,
        DummyRepository,
    )


def test_clear():

    manager = RepositoryManager()

    manager.register(
        "one",
        DummyRepository(),
    )

    manager.register(
        "two",
        DummyRepository(),
    )

    manager.clear()

    assert manager.size() == 0


def test_identifiers():

    manager = RepositoryManager()

    manager.register(
        "b",
        DummyRepository(),
    )

    manager.register(
        "a",
        DummyRepository(),
    )

    assert manager.identifiers() == (
        "a",
        "b",
    )
