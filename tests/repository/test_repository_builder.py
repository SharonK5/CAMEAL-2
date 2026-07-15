"""
===============================================================================
Tests for repository.repository_builder

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

import pytest

from repository.repository import Repository
from repository.repository_builder import RepositoryBuilder
from repository.repository_provider import RepositoryProvider


class DummyProvider(RepositoryProvider):

    @property
    def provider_name(self):
        return "Memory"

    @property
    def provider_type(self):
        return "memory"

    @property
    def connected(self):
        return True

    def connect(self):
        pass

    def disconnect(self):
        pass

    def exists(self, identifier):
        return False

    def load(self, identifier):
        raise KeyError(identifier)

    def save(self, asset):
        pass

    def delete(self, identifier):
        pass

    def search(self, query):
        return ()

    def identifiers(self):
        return ()

    def clear(self):
        pass

    def size(self):
        return 0


class DummyRepository(Repository):

    provider = None

    @property
    def name(self):
        return "Dummy Repository"

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


def test_build_repository():

    repository = DummyRepository()

    built = (
        RepositoryBuilder()
        .repository(repository)
        .build()
    )

    assert built is repository


def test_build_with_provider():

    repository = DummyRepository()

    provider = DummyProvider()

    built = (
        RepositoryBuilder()
        .repository(repository)
        .provider(provider)
        .build()
    )

    assert built.provider is provider


def test_repository_required():

    with pytest.raises(ValueError):

        RepositoryBuilder().build()


def test_builder_returns_repository():

    repository = DummyRepository()

    result = (
        RepositoryBuilder()
        .repository(repository)
        .build()
    )

    assert isinstance(
        result,
        Repository,
    )
