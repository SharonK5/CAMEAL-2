# kernel/workflows/base/workflow.py
"""
Workflow data model.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from .step import Step


@dataclass
class Workflow:
    """
    A declarative execution graph.

    A workflow defines the ordered sequence of steps to execute.
    Each step references a plugin-provided engine or task.
    """

    name: str
    steps: List[Step]
    description: Optional[str] = None
    version: str = "1.0.0"
    metadata: Dict[str, Any] = field(default_factory=dict)
    default: bool = False

    @property
    def step_names(self) -> List[str]:
        """Return the names of all steps in order."""
        return [step.name for step in self.steps]

    @property
    def plugin_names(self) -> List[str]:
        """Return all plugin names referenced by steps."""
        return list({step.plugin for step in self.steps if step.plugin})

    def __len__(self) -> int:
        return len(self.steps)

    def __repr__(self) -> str:
        return f"<Workflow name={self.name}, steps={len(self.steps)}>"
