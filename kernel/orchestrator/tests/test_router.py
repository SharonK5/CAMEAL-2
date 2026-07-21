# kernel/orchestrator/tests/test_router.py
import pytest
from unittest.mock import Mock
from uuid import uuid4

from kernel.orchestrator.router import Router
from kernel.orchestrator.exceptions import WorkflowNotFoundError
from kernel.models import Request


class TestRouter:
    def test_select_workflow_explicit(self):
        workflow_manager = Mock()
        workflow_manager.has.return_value = True

        router = Router(workflow_manager)
        request = Request(request_id=uuid4(), workflow_name="qa_workflow")
        context = Mock()

        result = router.select_workflow(request, context)
        assert result == "qa_workflow"

    def test_select_workflow_explicit_missing(self):
        workflow_manager = Mock()
        workflow_manager.has.return_value = False

        router = Router(workflow_manager)
        request = Request(request_id=uuid4(), workflow_name="missing_workflow")
        context = Mock()

        with pytest.raises(WorkflowNotFoundError):
            router.select_workflow(request, context)

    def test_select_workflow_default(self):
        workflow_manager = Mock()
        default_workflow = Mock()
        default_workflow.name = "default_workflow"
        workflow_manager.get_default.return_value = default_workflow

        router = Router(workflow_manager)
        request = Request(request_id=uuid4(), workflow_name=None)
        context = Mock()

        result = router.select_workflow(request, context)
        assert result == "default_workflow"

    def test_select_workflow_no_default(self):
        workflow_manager = Mock()
        workflow_manager.get_default.return_value = None

        router = Router(workflow_manager)
        request = Request(request_id=uuid4(), workflow_name=None)
        context = Mock()

        with pytest.raises(WorkflowNotFoundError):
            router.select_workflow(request, context)
