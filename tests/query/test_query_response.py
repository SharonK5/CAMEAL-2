"""
===============================================================================
Tests for query.query_response
===============================================================================
"""

import pytest

from query.query_response import QueryResponse


def make_response():

    return QueryResponse(
        identifier="response-001",
        success=True,
        message="Completed",
    )


def test_identifier():

    assert make_response().identifier == "response-001"


def test_success():

    assert make_response().success is True


def test_confidence():

    assert make_response().confidence == 1.0


def test_invalid_confidence():

    with pytest.raises(ValueError):

        QueryResponse(
            identifier="x",
            success=True,
            confidence=2.0,
        )


def test_negative_execution_time():

    with pytest.raises(ValueError):

        QueryResponse(
            identifier="x",
            success=True,
            execution_time=-1,
        )


def test_metadata_lookup():

    response = QueryResponse(
        identifier="x",
        success=True,
        metadata=(
            ("engine", "RAG"),
        ),
    )

    assert response.get_metadata(
        "engine"
    ) == "RAG"


def test_to_dict():

    data = make_response().to_dict()

    assert data["identifier"] == "response-001"


def test_from_dict():

    response = QueryResponse.from_dict(
        {
            "identifier": "response-001",
            "success": True,
            "message": "Completed",
            "results": [],
            "repositories": [],
            "metadata": {},
            "confidence": 0.95,
            "execution_time": 0.25,
        }
    )

    assert response.confidence == 0.95
