# kernel/managers/workflow_manager.py
"""
Workflow Manager – selects and executes workflows.
"""

from typing import Any, Dict, List, Optional
from ..models import Request, ExecutionPlan   # ✅ changed from ..orchestrator
from .manager import Manager
from .exceptions import ManagerResolutionError, ManagerValidationError


class WorkflowManager(Manager):
    """
    Manages workflow definitions and selection.

    Responsibilities:
        - Register workflows by name.
        - Select a workflow based on request metadata.
        - Execute a workflow plan.
    """

    def __init__(self) -> None:
        super().__init__("workflow_manager")
        self._default_workflow: Optional[str] = None

    def register(self, name: str, plan: ExecutionPlan, default: bool = False) -> None:
        """
        Register a workflow execution plan.

        Args:
            name: Unique name for the workflow.
            plan: The ExecutionPlan to associate with this workflow.
            default: If True, this workflow becomes the default.
        """
        self._validator.validate_name(name)
        self._validator.validate_not_none(plan, "plan")
        super().register(name, plan)
        if default:
            self._default_workflow = name

    def get_plan(self, request: Request) -> ExecutionPlan:
        """
        Select a workflow plan for the given request.

        The selection logic is:
            1. If the request specifies a workflow name, use it.
            2. If a default workflow is set, use it.
            3. If only one workflow is registered, use it.
            4. Otherwise, raise an error (selection logic must be customized).

        Override this method to implement custom selection logic.

        Args:
            request: The incoming request.

        Returns:
            The selected ExecutionPlan.

        Raises:
            ManagerResolutionError: If no workflow can be selected.
        """
        if len(self._registry) == 0:
            raise ManagerResolutionError("No workflows registered")

        # 1. Explicit workflow name from request (if available)
        if hasattr(request, 'workflow_name') and request.workflow_name:
            if self._registry.has(request.workflow_name):
                return self._registry.get(request.workflow_name)
            raise ManagerResolutionError(f"Workflow '{request.workflow_name}' not found")

        # 2. Default workflow
        if self._default_workflow:
            return self._registry.get(self._default_workflow)

        # 3. Only one workflow registered
        if len(self._registry) == 1:
            return self._registry.get(self._registry.list()[0])

        # 4. Multiple workflows and no selection criteria
        raise ManagerResolutionError(
            "Workflow selection logic not implemented; multiple workflows registered"
        )

    def __len__(self) -> int:
        """Return the number of registered workflows."""
        return len(self._registry)
