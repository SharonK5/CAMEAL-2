"""
===============================================================================
Tests for query.query

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from query.query import Query
from query.query_intent import QueryIntent


class DummyQuery(Query):

    @property
    def identifier(self) -> str:
        return "query-001"

    @property
    def intent(self) -> QueryIntent:
        return QueryIntent.RETRIEVE

    @property
    def source(self) -> str:
        return "unit-test"

    @property
    def description(self) -> str:
        return "Dummy query"

    @property
    def version(self) -> str:
        return "1.0.0"


def test_identifier():

    query = DummyQuery()

    assert query.identifier == "query-001"


def test_intent():

    query = DummyQuery()

    assert query.intent is QueryIntent.RETRIEVE


def test_source():

    query = DummyQuery()

    assert query.source == "unit-test"


def test_description():

    query = DummyQuery()

    assert query.description == "Dummy query"


def test_version():

    query = DummyQuery()

    assert query.version == "1.0.0"
