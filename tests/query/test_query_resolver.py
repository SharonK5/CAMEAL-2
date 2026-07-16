"""
===============================================================================
Tests for query.query_resolver
===============================================================================
"""

import pytest

from query.query_builder import QueryBuilder
from query.query_intent import QueryIntent
from query.query_registry import QueryRegistry
from query.query_resolver import QueryResolver
from query.query_request import QueryRequest


def make_query(identifier="query001", query_text="Test query"):
    return (
        QueryBuilder()
        .identifier(identifier)
        .intent(QueryIntent.RETRIEVE)
        .query(query_text)
        .build()
    )


def test_resolve():
    registry = QueryRegistry()
    query = make_query()
    registry.register(query.identifier, query)
    resolver = QueryResolver(registry)
    resolved = resolver.resolve(query.identifier)
    assert resolved == query


def test_resolve_unknown():
    registry = QueryRegistry()
    resolver = QueryResolver(registry)
    with pytest.raises(KeyError):
        resolver.resolve("unknown")


def test_exists():
    registry = QueryRegistry()
    query = make_query()
    registry.register(query.identifier, query)
    resolver = QueryResolver(registry)
    assert resolver.exists(query.identifier)


def test_exists_unknown():
    registry = QueryRegistry()
    resolver = QueryResolver(registry)
    assert not resolver.exists("unknown")


def test_resolve_many():
    registry = QueryRegistry()
    q1 = make_query("q1", "Query one")
    q2 = make_query("q2", "Query two")
    registry.register(q1.identifier, q1)
    registry.register(q2.identifier, q2)
    resolver = QueryResolver(registry)
    results = resolver.resolve_many(["q1", "q2"])
    assert results == (q1, q2)   # ← changed to tuple


def test_resolve_many_unknown():
    registry = QueryRegistry()
    q1 = make_query("q1", "Query one")
    registry.register(q1.identifier, q1)
    resolver = QueryResolver(registry)
    with pytest.raises(KeyError):
        resolver.resolve_many(["q1", "unknown"])
