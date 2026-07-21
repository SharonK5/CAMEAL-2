# kernel/orchestrator/tests/test_orchestrator.py
import pytest
from unittest.mock import Mock, patch
from uuid import uuid4

from kernel.orchestrator.orchestrator import Orchestrator
from kernel.orchestrator.exceptions import OrchestratorError, PlanValidationError
from kernel.models import Request
from kernel.lifecycle import HealthStatus


class TestOrchestrator:
    @pytest.fixture
    def mock_managers(self):
        workflow_manager = Mock()
        engine_manager = Mock()
        context_manager = Mock()
        return workflow_manager, engine_manager, context_manager

    @pytest.fixture
    def orchestrator(self, mock_managers):
        wf_mgr, eng_mgr, ctx_mgr = mock_managers
        return Orchestrator(wf_mgr, eng_mgr, ctx_mgr)

    def test_execute_success(self, orchestrator):
        """Should execute request and return response."""
        request = Request(
            request_id=uuid4(),
            workflow_name="test"
        )

        # Mock context building
        context = Mock()
        orchestrator._context_manager.build_from_request = Mock(return_value=context)

        # Mock router
        orchestrator._router.select_workflow = Mock(return_value="test")

        # Mock planner
        plan = Mock()
        plan.workflow_name = "test"
        plan.engine_names = ("a", "b")
        plan.metadata = {}
        orchestrator._planner.create_plan = Mock(return_value=plan)

        # Mock validator
        orchestrator._validator.validate = Mock()

        # Mock executor
        final_context = Mock()
        final_context.get = Mock(return_value="done")
        orchestrator._executor.execute = Mock(return_value=final_context)

        # Mock response builder
        with patch.object(orchestrator, '_build_response', return_value=Mock(status=200, result="done")):
            response = orchestrator.execute(request)

        assert response.status == 200
        assert response.result == "done"

    def test_validate_success(self, orchestrator):
        """Should return True for valid request."""
        request = Request(
            request_id=uuid4(),
            workflow_name="test"
        )

        orchestrator._context_manager.build_from_request = Mock(return_value=Mock())
        orchestrator._router.select_workflow = Mock(return_value="test")
        plan = Mock()
        plan.workflow_name = "test"
        plan.engine_names = ("a",)
        plan.metadata = {}
        orchestrator._planner.create_plan = Mock(return_value=plan)
        orchestrator._validator.validate = Mock()

        result = orchestrator.validate(request)
        assert result is True

    def test_validate_failure(self, orchestrator):
        """Should return False if plan validation fails."""
        request = Request(
            request_id=uuid4(),
            workflow_name="test"
        )

        orchestrator._context_manager.build_from_request = Mock(return_value=Mock())
        orchestrator._router.select_workflow = Mock(return_value="test")
        plan = Mock()
        plan.workflow_name = "test"
        plan.engine_names = ("missing",)
        plan.metadata = {}
        orchestrator._planner.create_plan = Mock(return_value=plan)
        orchestrator._validator.validate = Mock(side_effect=PlanValidationError("invalid"))

        result = orchestrator.validate(request)
        assert result is False

    def test_health_all_healthy(self, orchestrator):
        orchestrator._engine_manager.health_all = Mock(return_value={
            "engine1": HealthStatus.HEALTHY
        })
        orchestrator._workflow_manager.health = Mock(return_value=HealthStatus.HEALTHY)
        orchestrator._context_manager.health = Mock(return_value=HealthStatus.HEALTHY)

        assert orchestrator.health() == HealthStatus.HEALTHY

    def test_health_unhealthy_engine(self, orchestrator):
        orchestrator._engine_manager.health_all = Mock(return_value={
            "engine1": HealthStatus.UNHEALTHY
        })
        assert orchestrator.health() == HealthStatus.UNHEALTHY

    def test_start_stop(self, orchestrator):
        orchestrator.start()
        assert orchestrator._running is True

        orchestrator.stop()
        assert orchestrator._running is False
