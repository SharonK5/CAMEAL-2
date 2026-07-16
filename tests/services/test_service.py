"""
===============================================================================
Tests for services.service

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

import pytest

from services.service import Service


class DummyService(Service):
    """
    Concrete implementation for testing.
    """

    def __init__(self) -> None:
        self._initialized = False

    @property
    def name(self) -> str:
        return "dummy"

    def initialize(self) -> None:
        self._initialized = True

    def shutdown(self) -> None:
        self._initialized = False


# -----------------------------------------------------------------------------
# Name
# -----------------------------------------------------------------------------

def test_name():

    service = DummyService()

    assert service.name == "dummy"


# -----------------------------------------------------------------------------
# Initialization
# -----------------------------------------------------------------------------

def test_initialized_default():

    service = DummyService()

    assert service.initialized is False


def test_initialize():

    service = DummyService()

    service.initialize()

    assert service.initialized is True


def test_shutdown():

    service = DummyService()

    service.initialize()

    service.shutdown()

    assert service.initialized is False


# -----------------------------------------------------------------------------
# ensure_initialized()
# -----------------------------------------------------------------------------

def test_ensure_initialized_success():

    service = DummyService()

    service.initialize()

    service.ensure_initialized()


def test_ensure_initialized_failure():

    service = DummyService()

    with pytest.raises(RuntimeError):

        service.ensure_initialized()


# -----------------------------------------------------------------------------
# repr
# -----------------------------------------------------------------------------

def test_repr():

    service = DummyService()

    representation = repr(service)

    assert "DummyService" in representation

    assert "dummy" in representation

    assert "initialized=False" in representation


def test_repr_initialized():

    service = DummyService()

    service.initialize()

    representation = repr(service)

    assert "initialized=True" in representation
