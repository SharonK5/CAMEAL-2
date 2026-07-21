# kernel/context/workflow_context.py
"""
Workflow context – current workflow state.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from .exceptions import ContextValidationError


@dataclass(frozen=True)
class WorkflowContext:
    """
    Immutable workflow context.

    Attributes:
        workflow_id: Unique workflow identifier.
        workflow_name: Name of the workflow.
        step_index: Current step index.
        step_history: History of completed steps.
        status: Current workflow status.
        metadata: Additional workflow metadata.
    """

    workflow_id: str = ""
    workflow_name: str = ""
    step_index: int = 0
    step_history: List[str] = field(default_factory=list)
    status: str = "pending"
    metadata: Dict[str, str] = field(default_factory=dict)

    def add_step(self, step_name: str) -> "WorkflowContext":
        """Create a new context with an added step."""
        new_history = list(self.step_history) + [step_name]
        return WorkflowContext(
            workflow_id=self.workflow_id,
            workflow_name=self.workflow_name,
            step_index=len(new_history),
            step_history=new_history,
            status=self.status,
            metadata=self.metadata,
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "workflow_id": self.workflow_id,
            "workflow_name": self.workflow_name,
            "step_index": str(self.step_index),
            "step_history": list(self.step_history),
            "status": self.status,
            **self.metadata,
        }
