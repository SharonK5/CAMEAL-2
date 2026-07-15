from query.query_intent import QueryIntent
from query.query_request import QueryRequest


def make_request():

    return QueryRequest(
        identifier="q1",
        intent=QueryIntent.RETRIEVE,
        query="Retrieve climate policy",
    )


def test_identifier():

    assert make_request().identifier == "q1"


def test_query():

    assert make_request().query == "Retrieve climate policy"


def test_intent():

    assert make_request().intent is QueryIntent.RETRIEVE


def test_empty_identifier():

    import pytest

    with pytest.raises(ValueError):

        QueryRequest(
            identifier="",
            intent=QueryIntent.RETRIEVE,
            query="test",
        )


def test_empty_query():

    import pytest

    with pytest.raises(ValueError):

        QueryRequest(
            identifier="q1",
            intent=QueryIntent.RETRIEVE,
            query="",
        )


def test_parameter_lookup():

    request = QueryRequest(
        identifier="q1",
        intent=QueryIntent.RETRIEVE,
        query="policy",
        parameters=(("year", 2025),),
    )

    assert request.get_parameter("year") == 2025


def test_metadata_lookup():

    request = QueryRequest(
        identifier="q1",
        intent=QueryIntent.RETRIEVE,
        query="policy",
        metadata=(("user", "admin"),),
    )

    assert request.get_metadata("user") == "admin"


def test_to_dict():

    request = make_request()

    data = request.to_dict()

    assert data["identifier"] == "q1"


def test_from_dict():

    request = QueryRequest.from_dict(
        {
            "identifier": "q1",
            "intent": "RETRIEVE",
            "query": "Retrieve climate policy",
            "repositories": [],
            "parameters": {},
            "metadata": {},
            "priority": 0,
        }
    )

    assert request.identifier == "q1"
