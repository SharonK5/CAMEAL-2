import pytest
from unittest.mock import Mock

from query.execution.context_keys import ContextKeys
from query.execution.contracts import SecurityResult
from query.execution.execution_context import ExecutionContext
from query.execution.security_stage import SecurityStage
from query.query_intent import QueryIntent
from query.query_request import QueryRequest


def test_security_stage_execute_success():
    # Arrange
    request = QueryRequest(
        identifier="test-1",
        intent=QueryIntent.RETRIEVE,
        query="test query",
    )
    context = ExecutionContext()
    expected_result = SecurityResult(success=True, stage="security", allowed=True)
    mock_service = Mock()
    mock_service.authorize.return_value = expected_result  # matches stage

    stage = SecurityStage(mock_service)

    # Act
    result = stage.execute(request, context)

    # Assert
    assert result is expected_result
    assert context.get(ContextKeys.SECURITY_RESULT) is expected_result
    mock_service.authorize.assert_called_once_with(request)


def test_security_stage_name():
    stage = SecurityStage(Mock())
    assert stage.name == "security"
