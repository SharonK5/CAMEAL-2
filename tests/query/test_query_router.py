"""
===============================================================================
Tests for query.query_router
===============================================================================
"""

import pytest

from query.query_intent import QueryIntent
from query.query_request import QueryRequest
from query.query_response import QueryResponse
from query.query_router import QueryRouter


def handler(request):

    return QueryResponse(
        identifier=request.identifier,
        success=True,
        message="Handled",
    )


def make_request():

    return QueryRequest(
        identifier="Q001",
        intent=QueryIntent.RETRIEVE,
        query="Retrieve policies",
    )


def test_register():

    router = QueryRouter()

    router.register(
        QueryIntent.RETRIEVE,
        handler,
    )

    assert router.contains(
        QueryIntent.RETRIEVE
    )


def test_duplicate_registration():

    router = QueryRouter()

    router.register(
        QueryIntent.RETRIEVE,
        handler,
    )

    with pytest.raises(ValueError):

        router.register(
            QueryIntent.RETRIEVE,
            handler,
        )


def test_route():

    router = QueryRouter()

    router.register(
        QueryIntent.RETRIEVE,
        handler,
    )

    response = router.route(
        make_request()
    )

    assert response.success


def test_missing_handler():

    router = QueryRouter()

    with pytest.raises(KeyError):

        router.route(
            make_request()
        )


def test_unregister():

    router = QueryRouter()

    router.register(
        QueryIntent.RETRIEVE,
        handler,
    )

    router.unregister(
        QueryIntent.RETRIEVE
    )

    assert not router.contains(
        QueryIntent.RETRIEVE
    )


def test_clear():

    router = QueryRouter()

    router.register(
        QueryIntent.RETRIEVE,
        handler,
    )

    router.clear()

    assert router.count() == 0


def test_count():

    router = QueryRouter()

    router.register(
        QueryIntent.RETRIEVE,
        handler,
    )

    assert router.count() == 1
