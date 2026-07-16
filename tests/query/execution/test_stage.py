from query.execution.stage import ExecutionStage
from query.execution.execution_context import ExecutionContext

from query.query_request import QueryRequest
from query.query_response import QueryResponse
from query.query_intent import QueryIntent


class DummyStage(ExecutionStage):

    @property
    def name(self):

        return "dummy"

    def execute(self, request, context):

        context.set("executed", True)

        return None


def make_request():

    return QueryRequest(
        identifier="q1",
        intent=QueryIntent.RETRIEVE,
        query="test",
    )


def test_stage_name():

    stage = DummyStage()

    assert stage.name == "dummy"


def test_stage_execute():

    stage = DummyStage()

    context = ExecutionContext()

    response = stage.execute(
        make_request(),
        context,
    )

    assert response is None

    assert context.get("executed")
