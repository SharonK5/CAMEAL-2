"""
===============================================================================
Tests for query.query_registry
===============================================================================
"""

import pytest

from query.query_builder import QueryBuilder
from query.query_intent import QueryIntent
from query.query_registry import QueryRegistry
from query.query_request import QueryRequest


def make_query(identifier="query001", query_text="test query"):
    """Helper to build a QueryRequest using the fluent builder."""
    return (
        QueryBuilder()
        .identifier(identifier)
        .intent(QueryIntent.RETRIEVE)
        .query(query_text)
        .build()
    )


def test_register():
    registry = QueryRegistry()
    registry.register("query001", make_query())
    assert registry.contains("query001")


def test_get():
    registry = QueryRegistry()
    query = make_query()
    registry.register("query001", query)
    assert registry.get("query001") == query


def test_contains():
    registry = QueryRegistry()
    registry.register("query001", make_query())
    assert registry.contains("query001")


def test_duplicate_registration():
    registry = QueryRegistry()
    registry.register("query001", make_query())
    with pytest.raises(KeyError):
        registry.register("query001", make_query())


def test_unregister():
    registry = QueryRegistry()
    registry.register("query001", make_query())
    registry.unregister("query001")
    assert not registry.contains("query001")


def test_identifiers():
    registry = QueryRegistry()
    registry.register("b", make_query("query001"))
    registry.register(
        "a",
        make_query(identifier="query002", query_text="Assessment"),
    )
    # Identifiers are sorted
    assert registry.identifiers() == ("a", "b")


def test_clear():
    registry = QueryRegistry()
    registry.register("query001", make_query())
    registry.clear()
    assert len(registry) == 0


def test_queries():
    registry = QueryRegistry()
    query = make_query()
    registry.register("query001", query)
    assert registry.queries() == (query,)


def test_contains_operator():
    registry = QueryRegistry()
    registry.register("query001", make_query())
    assert "query001" in registry


def test_length():
    registry = QueryRegistry()
    registry.register("query001", make_query())
    assert len(registry) == 1
