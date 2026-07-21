# kernel/orchestrator/tests/test_dispatcher.py
"""Tests for the Dispatcher component."""

import pytest
from unittest.mock import Mock

from kernel.orchestrator.dispatcher import Dispatcher
from kernel.orchestrator.exceptions import EngineNotFoundError, DispatcherError


class TestDispatcher:
    def test_dispatch_success(self):
        """Should invoke engine and return updated context."""
        engine_manager = Mock()
        engine = Mock()
        engine.execute.return_value = "updated_context"

        engine_manager.get.return_value = engine

        dispatcher = Dispatcher(engine_manager)
        context = Mock()
        result = dispatcher.dispatch("test_engine", context)

        assert result == "updated_context"
        engine.execute.assert_called_once_with(context)

    def test_dispatch_engine_not_found(self):
        """Should raise if engine doesn't exist."""
        engine_manager = Mock()
        engine_manager.get.return_value = None

        dispatcher = Dispatcher(engine_manager)
        context = Mock()

        with pytest.raises(EngineNotFoundError):
            dispatcher.dispatch("missing_engine", context)

    def test_dispatch_engine_execution_fails(self):
        """Should raise DispatcherError if engine execution fails."""
        engine_manager = Mock()
        engine = Mock()
        engine.execute.side_effect = RuntimeError("engine failed")
        engine_manager.get.return_value = engine

        dispatcher = Dispatcher(engine_manager)
        context = Mock()

        with pytest.raises(DispatcherError):
            dispatcher.dispatch("test_engine", context)
