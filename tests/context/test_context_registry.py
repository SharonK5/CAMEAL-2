"""
===============================================================================
Tests for context.context_registry

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

import pytest

from context.context_builder import ContextBuilder
from context.context_registry import ContextRegistry
from context.institutional import InstitutionalContext
from context.jurisdictional import JurisdictionalContext
from context.operational import OperationalContext
from context.spatial import SpatialContext
from context.temporal import TemporalContext


def make_context():
    # InstitutionalContext now requires an identifier
    return ContextBuilder().build(
        institutional=InstitutionalContext(identifier="test"),
        jurisdictional=JurisdictionalContext(),
        spatial=SpatialContext(),
        temporal=TemporalContext(),
        operational=OperationalContext(),
    )


def test_register():
    registry = ContextRegistry()
    registry.register("ctx1", make_context())
    assert len(registry) == 1


def test_get():
    registry = ContextRegistry()
    context = make_context()
    registry.register("ctx1", context)
    assert registry.get("ctx1") == context


def test_contains():
    registry = ContextRegistry()
    registry.register("ctx1", make_context())
    assert registry.contains("ctx1")
    assert not registry.contains("ctx2")


def test_duplicate_registration():
    registry = ContextRegistry()
    registry.register("ctx1", make_context())
    with pytest.raises(ValueError):
        registry.register("ctx1", make_context())


def test_unregister():
    registry = ContextRegistry()
    registry.register("ctx1", make_context())
    registry.unregister("ctx1")
    assert registry.get("ctx1") is None


def test_identifiers():
    registry = ContextRegistry()
    registry.register("b", make_context())
    registry.register("a", make_context())
    assert registry.identifiers() == ("a", "b")


def test_clear():
    registry = ContextRegistry()
    registry.register("ctx1", make_context())
    registry.register("ctx2", make_context())
    registry.clear()
    assert len(registry) == 0


def test_contexts():
    registry = ContextRegistry()
    registry.register("ctx1", make_context())
    registry.register("ctx2", make_context())
    assert len(registry.contexts()) == 2
