"""
===============================================================================
Tests for repository.repository

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

import pytest

from repository.repository import Repository


class DummyRepository(Repository):
    """
    Minimal implementation for testing the abstract interface.
    """

    @property
    def name(self) -> str:
        return "Dummy"

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


def test_name():

    repo = DummyRepository()

    assert repo.name == "Dummy"


def test_version():

    repo = DummyRepository()

    assert repo.version == "1.0.0"


def test_contains():

    repo = DummyRepository()

    assert repo.contains("policy1") is False


def test_get_unknown():

    repo = DummyRepository()

    with pytest.raises(KeyError):
        repo.get("missing")


def test_list():

    repo = DummyRepository()

    assert tuple(repo.list()) == ()


def test_search():

    repo = DummyRepository()

    assert tuple(repo.search("climate")) == ()


def test_size():

    repo = DummyRepository()

    assert repo.size() == 0


def test_register():

    repo = DummyRepository()

    repo.register(object())


def test_unregister():

    repo = DummyRepository()

    repo.unregister("policy1")


def test_clear():

    repo = DummyRepository()

    repo.clear()
