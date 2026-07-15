"""
===============================================================================
Tests for repository.repository_registry

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

import pytest

from repository.repository import Repository
from repository.repository_registry import RepositoryRegistry


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


def make_repository():
    return DummyRepository()


def test_register():

    registry = RepositoryRegistry()

    registry.register(
        "main",
        make_repository(),
    )

    assert registry.size() == 1


def test_get():

    registry = RepositoryRegistry()

    repo = make_repository()

    registry.register("main", repo)

    assert registry.get("main") is repo


def test_contains():

    registry = RepositoryRegistry()

    registry.register(
        "main",
        make_repository(),
    )

    assert registry.contains("main")


def test_duplicate_registration():

    registry = RepositoryRegistry()

    registry.register(
        "main",
        make_repository(),
    )

    with pytest.raises(ValueError):

        registry.register(
            "main",
            make_repository(),
        )


def test_unregister():

    registry = RepositoryRegistry()

    registry.register(
        "main",
        make_repository(),
    )

    registry.unregister("main")

    assert registry.size() == 0


def test_identifiers():

    registry = RepositoryRegistry()

    registry.register("b", make_repository())
    registry.register("a", make_repository())

    assert registry.identifiers() == (
        "a",
        "b",
    )


def test_clear():

    registry = RepositoryRegistry()

    registry.register("a", make_repository())
    registry.register("b", make_repository())

    registry.clear()

    assert registry.size() == 0


def test_repositories():

    registry = RepositoryRegistry()

    r1 = make_repository()
    r2 = make_repository()

    registry.register("a", r1)
    registry.register("b", r2)

    assert len(registry.repositories()) == 2


def test_unknown_repository():

    registry = RepositoryRegistry()

    assert registry.get("missing") is None
