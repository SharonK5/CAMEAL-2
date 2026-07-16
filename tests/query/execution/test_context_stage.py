import pytest
from unittest.mock import Mock

from query.execution import ContextStage, ExecutionContext, ContextKeys
from query.execution.contracts import StageResult
from query.query_request import QueryRequest
from query.query_intent import QueryIntent
from context import GovernanceContext


class DummyContextResolver:
    def resolve(self, request):
        # Use correct field names
        return GovernanceContext(
            jurisdictional="US",
            institutional="CAMEAL",
            operational="query",
        )


def test_context_stage_uses_request_context():
    resolver = DummyContextResolver()
    stage = ContextStage(resolver)
    request = QueryRequest(
        identifier="1",
        intent=QueryIntent.RETRIEVE,
        query="climate",
        context=GovernanceContext(
            jurisdictional="EU",
            institutional="Test",
            operational="test",
        ),
    )
    context = ExecutionContext()

    result = stage.execute(request, context)

    assert result.success
    stored_context = context.get(ContextKeys.GOVERNANCE_CONTEXT)
    assert stored_context is request.context
    assert result.get_metadata("resolved") is True


def test_context_stage_resolves_if_no_context():
    resolver = DummyContextResolver()
    stage = ContextStage(resolver)
    request = QueryRequest(
        identifier="1",
        intent=QueryIntent.RETRIEVE,
        query="climate",
        context=None,
    )
    context = ExecutionContext()

    result = stage.execute(request, context)

    assert result.success
    stored_context = context.get(ContextKeys.GOVERNANCE_CONTEXT)
    assert stored_context is not None
    assert stored_context.jurisdictional == "US"


def test_context_stage_name():
    resolver = DummyContextResolver()
    stage = ContextStage(resolver)
    assert stage.name == "context"
