# kernel/orchestrator/router.py
"""
Internal routing component for the orchestrator.
"""

from typing import Optional, TYPE_CHECKING

from ..models import Request
from ..context import ExecutionContext
from .exceptions import WorkflowNotFoundError

if TYPE_CHECKING:
    from ..managers import WorkflowManager


class Router:
    def __init__(self, workflow_manager: "WorkflowManager") -> None:
        self._workflow_manager = workflow_manager

    def select_workflow(self, request: Request, context: ExecutionContext) -> str:
        if request.workflow_name:
            if self._workflow_manager.has(request.workflow_name):
                return request.workflow_name
            raise WorkflowNotFoundError(
                f"Specified workflow '{request.workflow_name}' not found"
            )

        default_workflow = self._workflow_manager.get_default()
        if default_workflow:
            # Return the name of the default workflow
            return default_workflow.name

        raise WorkflowNotFoundError(
            "No workflow specified in request and no default workflow registered"
        )
