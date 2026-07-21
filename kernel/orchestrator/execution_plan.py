# kernel/orchestrator/execution_plan.py
"""
Execution plan – ordered steps for a workflow.
"""

from typing import List, Any, Optional
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExecutionPlan:
    """
    Immutable execution plan for a workflow.

    Attributes:
        steps: Ordered list of steps (engines) to execute.
        name: Optional name of the plan.
        metadata: Additional metadata.
    """

    steps: List[Any] = field(default_factory=list)
    name: str = ""
    metadata: dict = field(default_factory=dict)

    @property
    def step_count(self) -> int:
        return len(self.steps)

    @property
    def is_empty(self) -> bool:
        return len(self.steps) == 0

    def add_step(self, step: Any) -> "ExecutionPlan":
        """Create a new plan with an added step."""
        return ExecutionPlan(
            steps=self.steps + [step],
            name=self.name,
            metadata=self.metadata,
        )
