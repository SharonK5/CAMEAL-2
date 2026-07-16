"""
===============================================================================
Tests for query.query_manager
===============================================================================
"""

import pytest

from query.query_builder import QueryBuilder
from query.query_intent import QueryIntent
from query.query_manager import QueryManager
from query.query_request import QueryRequest


def make_query(identifier="query001", query_text="Climate Search"):
    """Helper to build a QueryRequest."""
    return (
        QueryBuilder()
        .identifier(identifier)
        .intent(QueryIntent.RETRIEVE)
        .query(query_text)
        .build()
    )


def test_register():
    manager = QueryManager()
    query = make_query()
    manager.register(query)
    assert manager.contains(query.identifier)


def test_get():
    manager = QueryManager()
    query = make_query()
    manager.register(query)
    retrieved = manager.get(query.identifier)
    assert retrieved == query


def test_unregister():
    manager = QueryManager()
    query = make_query()
    manager.register(query)
    manager.unregister(query.identifier)
    assert not manager.contains(query.identifier)


def test_identifiers():
    manager = QueryManager()
    q1 = make_query("query001", "Climate Search")
    q2 = make_query("query002", "Assessment")
    manager.register(q1)
    manager.register(q2)
    # Manager may sort identifiers; we'll check set equality
    assert set(manager.identifiers()) == {"query001", "query002"}


def test_queries():
    manager = QueryManager()
    q1 = make_query("query001", "Climate Search")
    manager.register(q1)
    assert manager.queries() == (q1,)


def test_clear():
    manager = QueryManager()
    q1 = make_query("query001", "Climate Search")
    manager.register(q1)
    manager.clear()
    assert manager.count() == 0


def test_count():
    manager = QueryManager()
    q1 = make_query("query001", "Climate Search")
    manager.register(q1)
    assert manager.count() == 1
