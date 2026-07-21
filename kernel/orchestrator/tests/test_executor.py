# kernel/orchestrator/tests/test_executor.py
"""Tests for the Executor component."""

import pytest
from unittest.mock import Mock

from kernel.orchestrator.executor import Executor
from kernel.orchestrator.pipeline import Pipeline
from kernel.orchestrator.exceptions import ExecutionError


class TestExecutor:
    def test_execute_empty_pipeline(self):
        """Should return initial context unchanged."""
        dispatcher = Mock()
        executor = Executor(dispatcher)
        pipeline = Pipeline(workflow_name="test", stages=())
        context = Mock()

        result = executor.execute(pipeline, context)
        assert result == context
        dispatcher.dispatch.assert_not_called()

    def test_execute_success(self):
        """Should execute all stages in order."""
        dispatcher = Mock()
        dispatcher.dispatch.side_effect = ["ctx1", "ctx2", "ctx3"]

        executor = Executor(dispatcher)
        pipeline = Pipeline(workflow_name="test", stages=("a", "b", "c"))
        initial_context = Mock()

        result = executor.execute(pipeline, initial_context)

        assert result == "ctx3"
        assert dispatcher.dispatch.call_count == 3
        calls = dispatcher.dispatch.call_args_list
        assert calls[0][0] == ("a", initial_context)
        assert calls[1][0] == ("b", "ctx1")
        assert calls[2][0] == ("c", "ctx2")

    def test_execute_stage_failure(self):
        """Should stop on failure and raise ExecutionError."""
        dispatcher = Mock()
        dispatcher.dispatch.side_effect = ["ctx1", RuntimeError("engine failed")]

        executor = Executor(dispatcher)
        pipeline = Pipeline(workflow_name="test", stages=("a", "b"))
        initial_context = Mock()

        with pytest.raises(ExecutionError) as exc_info:
            executor.execute(pipeline, initial_context)

        assert "stage 'b'" in str(exc_info.value)
        assert dispatcher.dispatch.call_count == 2
