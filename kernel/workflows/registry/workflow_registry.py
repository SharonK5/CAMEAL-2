# kernel/workflows/registry/workflow_registry.py
"""
Thread-safe registry for workflows.
"""

from threading import RLock
from typing import Dict, List, Optional

from ..base.workflow import Workflow
from ..base.exceptions import WorkflowNotFoundError, WorkflowValidationError


class WorkflowRegistry:
    """
    Registry for all workflows.

    Thread-safe. Workflows are stored by name (string).
    """

    def __init__(self) -> None:
        self._workflows: Dict[str, Workflow] = {}
        self._default_workflow: Optional[str] = None
        self._lock = RLock()

    def register(self, workflow: Workflow, default: bool = False) -> None:
        """
        Register a workflow.

        Args:
            workflow: The workflow to register.
            default: If True, set this as the default workflow.

        Raises:
            WorkflowValidationError: If a workflow with the same name already exists.
        """
        with self._lock:
            if workflow.name in self._workflows:
                raise WorkflowValidationError(
                    f"Workflow '{workflow.name}' already registered"
                )
            self._workflows[workflow.name] = workflow
            if default or workflow.default:
                self._default_workflow = workflow.name

    def get(self, name: str) -> Workflow:
        """
        Retrieve a workflow by name.

        Args:
            name: Workflow identifier.

        Returns:
            The workflow instance.

        Raises:
            WorkflowNotFoundError: If no workflow is registered with that name.
        """
        with self._lock:
            if name not in self._workflows:
                raise WorkflowNotFoundError(f"Workflow '{name}' not found")
            return self._workflows[name]

    def get_default(self) -> Optional[Workflow]:
        """
        Return the default workflow.

        Returns:
            The default workflow, or None if no default is set.
        """
        with self._lock:
            if self._default_workflow:
                return self._workflows.get(self._default_workflow)
            # If only one workflow exists, return it
            if len(self._workflows) == 1:
                return next(iter(self._workflows.values()))
            return None

    def has(self, name: str) -> bool:
        """Check if a workflow exists."""
        with self._lock:
            return name in self._workflows

    def list(self) -> List[str]:
        """Return a list of all registered workflow names."""
        with self._lock:
            return sorted(self._workflows.keys())

    def all(self) -> List[Workflow]:
        """Return a list of all registered workflows."""
        with self._lock:
            return list(self._workflows.values())

    def __len__(self) -> int:
        with self._lock:
            return len(self._workflows)

    def __iter__(self):
        with self._lock:
            return iter(self._workflows.values())

    def clear(self) -> None:
        """Clear all registered workflows (primarily for testing)."""
        with self._lock:
            self._workflows.clear()
            self._default_workflow = None
