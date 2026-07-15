"""
===============================================================================
Tests for repository.repository_resolver

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

import pytest

from repository.repository import Repository
from repository.repository_registry import RepositoryRegistry
from repository.repository_resolver import RepositoryResolver


class DummyRepository(Repository):

    @property
    def name(self) -> str:
        return "Dummy Repository"

    @property
    def version(self) -> str:
        return "1.0.0"

    def contains(self, identifier: str) -> bool:
        return False

    def get(self, identifier: str):
        raise KeyError(identifier)

    def list(self):
        return ()

    def search(self, query: str):
        return ()

    def register(self, asset):
        pass

    def unregister(self, identifier: str):
        pass

    def clear(self):
        pass

    def size(self) -> int:
        return 0


def make_repository() -> Repository:
    return DummyRepository()


def test_resolve():

    registry = RepositoryRegistry()

    repository = make_repository()

    registry.register(
        "policy",
        repository,
    )

    resolver = RepositoryResolver(registry)

    assert resolver.resolve("policy") is repository


def test_unknown_repository():

    resolver = RepositoryResolver(
        RepositoryRegistry()
    )

    with pytest.raises(KeyError):

        resolver.resolve("missing")


def test_exists():

    registry = RepositoryRegistry()

    registry.register(
        "policy",
        make_repository(),
    )

    resolver = RepositoryResolver(registry)

    assert resolver.exists("policy")


def test_not_exists():

    resolver = RepositoryResolver(
        RepositoryRegistry()
    )

    assert not resolver.exists("missing")
