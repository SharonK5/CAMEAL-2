# kernel/workflows/base/step.py
"""
Step data model.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List


@dataclass
class Step:
    """
    A single execution step in a workflow.

    A step references a plugin that provides an engine or task.
    """

    name: str
    plugin: str  # The plugin providing the engine/task
    config: Dict[str, Any] = field(default_factory=dict)
    depends_on: Optional[List[str]] = None
    condition: Optional[str] = None
    on_failure: Optional[str] = None  # e.g., "skip", "fail", "retry"
    timeout: Optional[int] = None  # Seconds

    def __repr__(self) -> str:
        return f"<Step name={self.name}, plugin={self.plugin}>"
