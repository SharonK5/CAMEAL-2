"""
===============================================================================
Tests for repository.repository_factory
===============================================================================
"""

import pytest

from repository.repository import Repository
from repository.repository_factory import RepositoryFactory


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

    factory = RepositoryFactory()

    factory.register(
        "dummy",
        build_repository,
    )

    assert factory.size() == 1


def test_create():

    factory = RepositoryFactory()

    factory.register(
        "dummy",
        build_repository,
    )

    repository = factory.create("dummy")

    assert isinstance(
        repository,
        DummyRepository,
    )


def test_duplicate():

    factory = RepositoryFactory()

    factory.register(
        "dummy",
        build_repository,
    )

    with pytest.raises(ValueError):

        factory.register(
            "dummy",
            build_repository,
        )


def test_unknown():

    factory = RepositoryFactory()

    with pytest.raises(KeyError):

        factory.create("missing")


def test_contains():

    factory = RepositoryFactory()

    factory.register(
        "dummy",
        build_repository,
    )

    assert factory.contains(
        "dummy"
    )


def test_repository_types():

    factory = RepositoryFactory()

    factory.register("b", build_repository)
    factory.register("a", build_repository)

    assert factory.repository_types() == (
        "a",
        "b",
    )


def test_clear():

    factory = RepositoryFactory()

    factory.register(
        "dummy",
        build_repository,
    )

    factory.clear()

    assert factory.size() == 0
