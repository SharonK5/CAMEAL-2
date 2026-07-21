# kernel/orchestrator/plan.py
"""
Immutable execution plan for the orchestrator.

The plan defines the ordered sequence of engines to invoke
for a given workflow.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExecutionPlan:
    """
    An immutable execution plan.

    The plan contains:
    - The workflow name that generated it.
    - The ordered list of engine names.
    - Optional metadata (e.g., request ID, context version).

    The plan is created by the Planner and consumed by the Executor.
    It is never modified during execution.
    """

    workflow_name: str
    engine_names: Tuple[str, ...] = field(default_factory=tuple)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        # Ensure engine_names is a tuple (already enforced by default_factory)
        if not isinstance(self.engine_names, tuple):
            # This shouldn't happen if we use the constructor properly,
            # but we'll convert to tuple to guarantee immutability.
            object.__setattr__(self, 'engine_names', tuple(self.engine_names))

    @property
    def stages(self) -> Tuple[str, ...]:
        """Alias for engine_names."""
        return self.engine_names

    @property
    def is_empty(self) -> bool:
        """Return True if the plan has no engines to execute."""
        return len(self.engine_names) == 0

    def __len__(self) -> int:
        return len(self.engine_names)

    def __iter__(self):
        return iter(self.engine_names)

    def __repr__(self) -> str:
        return f"ExecutionPlan(workflow={self.workflow_name}, stages={list(self.engine_names)})"
