# kernel/managers/tests/test_workflow_manager.py
"""
Tests for WorkflowManager.
"""

import pytest
from uuid import uuid4

from kernel.managers.workflow_manager import WorkflowManager
from kernel.managers.exceptions import (
    ManagerResolutionError,
    ManagerValidationError,
    ManagerRegistrationError,
)
from kernel.models import ExecutionPlan, Request


class TestWorkflowManager:
    def test_register_get(self):
        mgr = WorkflowManager()
        plan = ExecutionPlan(workflow_name="test_wf", engine_names=("engine1", "engine2"))
        mgr.register("test_wf", plan)
        retrieved = mgr.get("test_wf")
        assert retrieved is plan

    def test_register_duplicate(self):
        mgr = WorkflowManager()
        plan = ExecutionPlan(workflow_name="test_wf", engine_names=("engine1",))
        mgr.register("test_wf", plan)
        with pytest.raises(ManagerRegistrationError):
            mgr.register("test_wf", plan)

    def test_get_plan_single(self):
        mgr = WorkflowManager()
        plan = ExecutionPlan(workflow_name="test_wf", engine_names=("engine1",))
        mgr.register("test_wf", plan)
        request = Request(request_id=uuid4())  # ✅ UUID
        selected = mgr.get_plan(request)
        assert selected is plan

    def test_get_plan_with_default(self):
        mgr = WorkflowManager()
        plan1 = ExecutionPlan(workflow_name="default_wf", engine_names=("engine1",))
        plan2 = ExecutionPlan(workflow_name="other_wf", engine_names=("engine2",))
        mgr.register("default_wf", plan1, default=True)
        mgr.register("other_wf", plan2)
        request = Request(request_id=uuid4())
        selected = mgr.get_plan(request)
        assert selected is plan1

    def test_get_plan_with_explicit_request_workflow(self):
        mgr = WorkflowManager()
        plan1 = ExecutionPlan(workflow_name="explicit_wf", engine_names=("engine1",))
        plan2 = ExecutionPlan(workflow_name="default_wf", engine_names=("engine2",))
        mgr.register("explicit_wf", plan1)
        mgr.register("default_wf", plan2, default=True)
        request = Request(
            request_id=uuid4(),
            workflow_name="explicit_wf"   # ✅ added
        )
        selected = mgr.get_plan(request)
        assert selected is plan1

    def test_get_plan_no_workflows(self):
        mgr = WorkflowManager()
        request = Request(request_id=uuid4())
        with pytest.raises(ManagerResolutionError):
            mgr.get_plan(request)

    def test_get_plan_multiple_no_default(self):
        mgr = WorkflowManager()
        plan1 = ExecutionPlan(workflow_name="wf1", engine_names=("engine1",))
        plan2 = ExecutionPlan(workflow_name="wf2", engine_names=("engine2",))
        mgr.register("wf1", plan1)
        mgr.register("wf2", plan2)
        request = Request(request_id=uuid4())
        with pytest.raises(ManagerResolutionError):
            mgr.get_plan(request)

    def test_len(self):
        mgr = WorkflowManager()
        assert len(mgr) == 0
        plan = ExecutionPlan(workflow_name="test", engine_names=())
        mgr.register("test", plan)
        assert len(mgr) == 1
