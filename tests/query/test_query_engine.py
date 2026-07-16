"""
===============================================================================
Tests for query.query_engine
===============================================================================
"""

import pytest

from query.query_engine import QueryEngine
from query.query_router import QueryRouter
from query.query_request import QueryRequest
from query.query_response import QueryResponse
from query.query_intent import QueryIntent


def make_request():

    return QueryRequest(
        identifier="query001",
        intent=QueryIntent.RETRIEVE,
        query="Retrieve climate policies",
    )


def handler(request: QueryRequest) -> QueryResponse:

    return QueryResponse(
        identifier=request.identifier,
        success=True,
        message="Executed successfully",
    )


def test_router_property():

    router = QueryRouter()

    engine = QueryEngine(router)

    assert engine.router is router


def test_execute():

    router = QueryRouter()

    router.register(
        QueryIntent.RETRIEVE,
        handler,
    )

    engine = QueryEngine(router)

    response = engine.execute(
        make_request()
    )

    assert response.success
    assert response.identifier == "query001"


def test_missing_handler():

    router = QueryRouter()

    engine = QueryEngine(router)

    with pytest.raises(KeyError):

        engine.execute(
            make_request()
        )


def test_multiple_execution():

    router = QueryRouter()

    router.register(
        QueryIntent.RETRIEVE,
        handler,
    )

    engine = QueryEngine(router)

    r1 = engine.execute(make_request())

    r2 = engine.execute(make_request())

    assert r1.success
    assert r2.success


def test_engine_is_reusable():

    router = QueryRouter()

    router.register(
        QueryIntent.RETRIEVE,
        handler,
    )

    engine = QueryEngine(router)

    for _ in range(5):

        response = engine.execute(
            make_request()
        )

        assert response.success
