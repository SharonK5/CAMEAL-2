# kernel/workflows/parser/validator.py
"""
Workflow validator.
"""

from typing import List, Set

from ..base.workflow import Workflow
from ..base.exceptions import WorkflowValidationError


class WorkflowValidator:
    """
    Validates workflow definitions.
    """

    @classmethod
    def validate(cls, workflow: Workflow) -> None:
        """
        Validate a workflow.

        Checks:
            - Workflow has at least one step.
            - All step names are unique.
            - All plugin references are valid (deferred to runtime).
            - Dependencies reference existing steps.
            - No circular dependencies.

        Args:
            workflow: The workflow to validate.

        Raises:
            WorkflowValidationError: If validation fails.
        """
        if not workflow.steps:
            raise WorkflowValidationError(
                f"Workflow '{workflow.name}' has no steps"
            )

        # Check unique step names
        names: List[str] = []
        for step in workflow.steps:
            if step.name in names:
                raise WorkflowValidationError(
                    f"Duplicate step name '{step.name}' in workflow '{workflow.name}'"
                )
            names.append(step.name)

        # Check dependencies reference existing steps
        step_names = set(names)
        for step in workflow.steps:
            if step.depends_on:
                for dep in step.depends_on:
                    if dep not in step_names:
                        raise WorkflowValidationError(
                            f"Step '{step.name}' depends on unknown step '{dep}'"
                        )

        # Check for circular dependencies
        cls._check_circular_dependencies(workflow)

    @classmethod
    def _check_circular_dependencies(cls, workflow: Workflow) -> None:
        """Detect circular dependencies between steps."""
        visited = set()
        path = set()

        def dfs(step_name: str) -> None:
            if step_name in path:
                raise WorkflowValidationError(
                    f"Circular dependency detected in workflow '{workflow.name}' "
                    f"involving step '{step_name}'"
                )
            if step_name in visited:
                return

            visited.add(step_name)
            path.add(step_name)

            step = next((s for s in workflow.steps if s.name == step_name), None)
            if step and step.depends_on:
                for dep in step.depends_on:
                    dfs(dep)

            path.remove(step_name)

        for step in workflow.steps:
            if step.name not in visited:
                dfs(step.name)
