"""
Tests for repository.repository_provider
"""

import pytest

from repository.repository_provider import RepositoryProvider


class DummyProvider(RepositoryProvider):

    def __init__(self):
        self._connected = False

    @property
    def provider_name(self):
        return "Dummy"

    @property
    def provider_type(self):
        return "memory"

    @property
    def connected(self):
        return self._connected

    def connect(self):
        self._connected = True

    def disconnect(self):
        self._connected = False

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


def test_provider_name():

    provider = DummyProvider()

    assert provider.provider_name == "Dummy"


def test_provider_type():

    provider = DummyProvider()

    assert provider.provider_type == "memory"


def test_connect():

    provider = DummyProvider()

    provider.connect()

    assert provider.connected


def test_disconnect():

    provider = DummyProvider()

    provider.connect()

    provider.disconnect()

    assert provider.connected is False


def test_exists():

    provider = DummyProvider()

    assert provider.exists("x") is False


def test_load_unknown():

    provider = DummyProvider()

    with pytest.raises(KeyError):
        provider.load("missing")


def test_search():

    provider = DummyProvider()

    assert tuple(provider.search("policy")) == ()


def test_identifiers():

    provider = DummyProvider()

    assert tuple(provider.identifiers()) == ()
