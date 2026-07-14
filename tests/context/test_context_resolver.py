"""
===============================================================================
Tests for context.context_resolver

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

import pytest

from context.context_builder import ContextBuilder
from context.context_registry import ContextRegistry
from context.context_resolver import ContextResolver
from context.institutional import InstitutionalContext
from context.jurisdictional import JurisdictionalContext
from context.spatial import SpatialContext
from context.temporal import TemporalContext
from context.operational import OperationalContext


def make_context():
    return ContextBuilder().build(
        institutional=InstitutionalContext(identifier="test"),
        jurisdictional=JurisdictionalContext(),
        spatial=SpatialContext(),
        temporal=TemporalContext(),
        operational=OperationalContext(),
    )


@pytest.fixture
def registry_with_contexts():
    registry = ContextRegistry()
    registry.register("ctx1", make_context())
    registry.register("ctx2", make_context())
    return registry


def test_resolve_exists(registry_with_contexts):
    resolver = ContextResolver(registry_with_contexts)
    context = resolver.resolve("ctx1")
    assert context is not None
    assert context == registry_with_contexts.get("ctx1")


def test_resolve_missing():
    registry = ContextRegistry()
    resolver = ContextResolver(registry)
    with pytest.raises(KeyError, match="Unknown context 'missing'"):
        resolver.resolve("missing")


def test_exists_true(registry_with_contexts):
    resolver = ContextResolver(registry_with_contexts)
    assert resolver.exists("ctx1") is True


def test_exists_false():
    registry = ContextRegistry()
    resolver = ContextResolver(registry)
    assert resolver.exists("nonexistent") is False


def test_resolve_returns_same_instance(registry_with_contexts):
    resolver = ContextResolver(registry_with_contexts)
    resolved = resolver.resolve("ctx1")
    stored = registry_with_contexts.get("ctx1")
    assert resolved is stored


def test_registry_property(registry_with_contexts):
    resolver = ContextResolver(registry_with_contexts)
    # The property returns the same registry instance
    assert resolver.registry is registry_with_contexts


def test_resolve_many_success(registry_with_contexts):
    resolver = ContextResolver(registry_with_contexts)
    contexts = resolver.resolve_many(("ctx1", "ctx2"))
    assert len(contexts) == 2
    assert contexts[0] == registry_with_contexts.get("ctx1")
    assert contexts[1] == registry_with_contexts.get("ctx2")


def test_resolve_many_raises_on_first_missing(registry_with_contexts):
    resolver = ContextResolver(registry_with_contexts)
    # The resolver processes in order, so it will stop at the first missing.
    with pytest.raises(KeyError, match="Unknown context 'missing'"):
        resolver.resolve_many(("ctx1", "missing", "ctx2"))
