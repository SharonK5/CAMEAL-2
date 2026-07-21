# kernel/orchestrator/pipeline.py
"""
Immutable execution pipeline for the orchestrator.

The pipeline represents the ordered sequence of engine names
to be invoked for a given workflow.

It is a pure data container and contains no execution logic.
"""

from typing import Tuple, Iterator, Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class Pipeline:
    """
    An immutable execution pipeline.

    The pipeline is created from an ExecutionPlan and provides
    ordered access to the engine names.

    Attributes:
        workflow_name: The name of the workflow that generated this pipeline.
        stages: A tuple of engine names in execution order.
        metadata: Optional additional data (e.g., request ID).
    """

    workflow_name: str
    stages: Tuple[str, ...]
    metadata: dict = None

    def __post_init__(self):
        # Ensure metadata is a dict (default to empty if None)
        if self.metadata is None:
            object.__setattr__(self, 'metadata', {})

    @property
    def is_empty(self) -> bool:
        """Return True if the pipeline has no stages."""
        return len(self.stages) == 0

    def __len__(self) -> int:
        return len(self.stages)

    def __iter__(self) -> Iterator[str]:
        return iter(self.stages)

    def __getitem__(self, index: int) -> str:
        return self.stages[index]

    def __repr__(self) -> str:
        return f"Pipeline(workflow={self.workflow_name}, stages={list(self.stages)})"
