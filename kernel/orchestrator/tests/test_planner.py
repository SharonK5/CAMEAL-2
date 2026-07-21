# kernel/orchestrator/tests/test_planner.py
"""Tests for the Planner component."""

import pytest
from unittest.mock import Mock

from kernel.orchestrator.planner import Planner
from kernel.orchestrator.exceptions import PlanValidationError


class TestPlanner:
    def test_create_plan_valid(self):
        """Should create an execution plan from a workflow."""
        workflow_manager = Mock()
        workflow = Mock()
        workflow.steps = ["security", "retrieval", "reasoning"]
        workflow_manager.get.return_value = workflow

        planner = Planner(workflow_manager)
        plan = planner.create_plan("test_workflow", "req-123")

        assert plan.workflow_name == "test_workflow"
        assert plan.engine_names == ("security", "retrieval", "reasoning")
        assert plan.metadata["request_id"] == "req-123"
        assert plan.metadata["total_steps"] == 3

    def test_create_plan_workflow_not_found(self):
        """Should raise if workflow doesn't exist."""
        workflow_manager = Mock()
        workflow_manager.get.return_value = None

        planner = Planner(workflow_manager)
        with pytest.raises(PlanValidationError):
            planner.create_plan("missing_workflow")

    def test_create_plan_no_steps(self):
        """Should raise if workflow has no steps."""
        workflow_manager = Mock()
        workflow = Mock()
        workflow.steps = []
        workflow_manager.get.return_value = workflow

        planner = Planner(workflow_manager)
        with pytest.raises(PlanValidationError):
            planner.create_plan("empty_workflow")

    def test_create_plan_deduplicates_engines(self):
        """Should remove duplicate engine names while preserving order."""
        workflow_manager = Mock()
        workflow = Mock()
        workflow.steps = ["engine_a", "engine_b", "engine_a", "engine_c"]
        workflow_manager.get.return_value = workflow

        planner = Planner(workflow_manager)
        plan = planner.create_plan("test_workflow")

        assert plan.engine_names == ("engine_a", "engine_b", "engine_c")

    def test_extract_engines_from_dict_steps(self):
        """Should extract engines from dict-style steps."""
        workflow_manager = Mock()
        workflow = Mock()
        workflow.steps = [
            {"engine": "security"},
            {"engine": "retrieval"},
        ]
        workflow_manager.get.return_value = workflow

        planner = Planner(workflow_manager)
        plan = planner.create_plan("test_workflow")
        assert plan.engine_names == ("security", "retrieval")
