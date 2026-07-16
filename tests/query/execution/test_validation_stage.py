from query.execution.execution_context import ExecutionContext
from query.execution.validation_stage import ValidationStage
from query.execution.context_keys import ContextKeys  # new import

from query.query_intent import QueryIntent
from query.query_request import QueryRequest
from query.query_validator import QueryValidator


def make_request():

    return QueryRequest(
        identifier="query-001",
        intent=QueryIntent.RETRIEVE,
        query="Climate policy",
    )


def test_name():

    stage = ValidationStage()

    assert stage.name == "validation"


def test_default_validator():

    stage = ValidationStage()

    assert isinstance(
        stage.validator,
        QueryValidator,
    )


def test_execute_sets_context():

    stage = ValidationStage()

    context = ExecutionContext()

    response = stage.execute(
        make_request(),
        context,
    )

    assert response is None

    # Updated to use ContextKeys instead of raw string
    assert context.get(
        ContextKeys.VALIDATED
    ) is True


def test_invalid_request_raises():

    stage = ValidationStage()

    context = ExecutionContext()

    request = QueryRequest(
        identifier="q",
        intent=QueryIntent.RETRIEVE,
        query="x",
        priority=-1,
    )

    import pytest

    with pytest.raises(ValueError):

        stage.execute(
            request,
            context,
        )
