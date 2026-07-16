"""
===============================================================================
Tests for query.query_validator
===============================================================================
"""

import pytest

from query.query_intent import QueryIntent
from query.query_request import QueryRequest
from query.query_validator import QueryValidator


def make_request():

    return QueryRequest(
        identifier="query-001",
        intent=QueryIntent.RETRIEVE,
        query="Retrieve climate policy",
    )


def test_validate():

    validator = QueryValidator()

    validator.validate(make_request())


def test_is_valid():

    validator = QueryValidator()

    assert validator.is_valid(make_request())


def test_invalid_type():

    validator = QueryValidator()

    with pytest.raises(TypeError):

        validator.validate("invalid")


def test_negative_priority():

    validator = QueryValidator()

    request = QueryRequest(
        identifier="q1",
        intent=QueryIntent.RETRIEVE,
        query="test",
        priority=-1,
    )

    with pytest.raises(ValueError):

        validator.validate(request)


def test_blank_repository():

    validator = QueryValidator()

    request = QueryRequest(
        identifier="q1",
        intent=QueryIntent.RETRIEVE,
        query="test",
        repositories=("policy", ""),
    )

    with pytest.raises(ValueError):

        validator.validate(request)


def test_blank_parameter():

    validator = QueryValidator()

    request = QueryRequest(
        identifier="q1",
        intent=QueryIntent.RETRIEVE,
        query="test",
        parameters=(("", "value"),),
    )

    with pytest.raises(ValueError):

        validator.validate(request)


def test_blank_metadata():

    validator = QueryValidator()

    request = QueryRequest(
        identifier="q1",
        intent=QueryIntent.RETRIEVE,
        query="test",
        metadata=(("", "value"),),
    )

    with pytest.raises(ValueError):

        validator.validate(request)


def test_invalid_returns_false():

    validator = QueryValidator()

    assert validator.is_valid("invalid") is False
