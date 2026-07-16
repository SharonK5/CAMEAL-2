import pytest
from unittest.mock import Mock

from query.execution import RoutingStage, ExecutionContext, ContextKeys
from query.execution.contracts import RoutingResult
from query.query_request import QueryRequest
from query.query_intent import QueryIntent


class DummyRouter:
    def handler(self, intent):
        return Mock(handle=lambda req: "result")


def test_routing_stage():
    router = DummyRouter()
    stage = RoutingStage(router)
    request = QueryRequest(
        identifier="1",
        intent=QueryIntent.RETRIEVE,
        query="climate",
    )
    context = ExecutionContext()

    result = stage.execute(request, context)

    assert result.success
    assert isinstance(result, RoutingResult)
    assert result.handler is not None
    assert context.get(ContextKeys.QUERY_HANDLER) is result.handler


def test_routing_stage_name():
    router = DummyRouter()
    stage = RoutingStage(router)
    assert stage.name == "routing"
