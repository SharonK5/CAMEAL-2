# kernel/orchestrator/planner.py
"""
Internal planner component.

Converts a workflow definition into an immutable ExecutionPlan.
"""

from typing import List, Optional
from ..managers import WorkflowManager
from .plan import ExecutionPlan
from .exceptions import PlanValidationError


class Planner:
    """
    Builds an execution plan from a workflow.

    The planner retrieves the workflow definition from the WorkflowManager,
    validates its structure, and produces an ordered list of engine names.

    The planner does not execute any engines.
    """

    def __init__(self, workflow_manager: WorkflowManager) -> None:
        self._workflow_manager = workflow_manager

    def create_plan(self, workflow_name: str, request_id: Optional[str] = None) -> ExecutionPlan:
        """
        Create an immutable execution plan for the given workflow.

        Args:
            workflow_name: The name of the workflow to plan.
            request_id: Optional identifier for the request (stored in metadata).

        Returns:
            ExecutionPlan: An immutable execution plan.

        Raises:
            PlanValidationError: If the workflow is invalid or has no steps.
        """
        workflow = self._workflow_manager.get(workflow_name)
        if not workflow:
            raise PlanValidationError(f"Workflow '{workflow_name}' not found")

        # Extract engine names from the workflow steps
        # Assumes workflow.steps is a list of dicts with "engine" key,
        # or a list of strings directly.
        engine_names = self._extract_engines(workflow)

        if not engine_names:
            raise PlanValidationError(f"Workflow '{workflow_name}' has no executable steps")

        # Remove duplicates while preserving order
        seen = set()
        unique_engines = []
        for name in engine_names:
            if name not in seen:
                seen.add(name)
                unique_engines.append(name)

        return ExecutionPlan(
            workflow_name=workflow_name,
            engine_names=tuple(unique_engines),
            metadata={
                "request_id": request_id,
                "total_steps": len(unique_engines),
            }
        )

    def _extract_engines(self, workflow) -> List[str]:
        """
        Extract engine names from a workflow definition.

        Supports two formats:
        1. workflow.steps is a list of strings (engine names).
        2. workflow.steps is a list of dicts with an "engine" key.
        """
        steps = getattr(workflow, "steps", [])
        if not steps:
            return []

        engines = []
        for step in steps:
            if isinstance(step, str):
                engines.append(step)
            elif isinstance(step, dict):
                engine = step.get("engine")
                if engine:
                    engines.append(engine)
            # If step is an object with a name or engine attribute, handle it?
            # For now, we assume simple formats.
        return engines
