"""
===============================================================================
Tests for repository.repository_validator

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

import pytest

from repository.repository import Repository
from repository.repository_validator import RepositoryValidator


class ValidRepository(Repository):

    @property
    def name(self):
        return "Policy Repository"

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


class EmptyNameRepository(ValidRepository):

    @property
    def name(self):
        return ""


class EmptyVersionRepository(ValidRepository):

    @property
    def version(self):
        return ""


def test_valid_repository():

    validator = RepositoryValidator()

    validator.validate(
        ValidRepository()
    )


def test_invalid_type():

    validator = RepositoryValidator()

    with pytest.raises(TypeError):
        validator.validate(object())


def test_empty_name():

    validator = RepositoryValidator()

    with pytest.raises(ValueError):
        validator.validate(
            EmptyNameRepository()
        )


def test_empty_version():

    validator = RepositoryValidator()

    with pytest.raises(ValueError):
        validator.validate(
            EmptyVersionRepository()
        )


def test_is_valid():

    validator = RepositoryValidator()

    assert validator.is_valid(
        ValidRepository()
    )


def test_is_not_valid():

    validator = RepositoryValidator()

    assert not validator.is_valid(
        EmptyNameRepository()
    )


def test_is_not_repository():

    validator = RepositoryValidator()

    assert not validator.is_valid(
        object()
    )
