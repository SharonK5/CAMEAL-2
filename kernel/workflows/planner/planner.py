# kernel/workflows/planner/planner.py
"""
Workflow planner – converts workflows into execution plans.
"""

from typing import List, Set, Dict
from collections import deque

from ..base.workflow import Workflow
from ..base.step import Step
from ..base.exceptions import WorkflowValidationError


class WorkflowPlanner:
    """
    Plans workflow execution by resolving dependencies and ordering steps.
    """

    @classmethod
    def plan(cls, workflow: Workflow) -> List[Step]:
        """
        Generate an execution plan (ordered list of steps).

        The plan respects dependencies and ensures each step
        is executed after its dependencies.

        Args:
            workflow: The workflow to plan.

        Returns:
            List of steps in execution order.

        Raises:
            WorkflowValidationError: If dependencies are invalid or circular.
        """
        # Build dependency graph
        step_map = {step.name: step for step in workflow.steps}
        dependencies = cls._build_dependencies(workflow, step_map)

        # Topological sort
        return cls._topological_sort(workflow, step_map, dependencies)

    @classmethod
    def _build_dependencies(
        cls,
        workflow: Workflow,
        step_map: Dict[str, Step]
    ) -> Dict[str, Set[str]]:
        """Build dependency graph."""
        dependencies = {}
        for step in workflow.steps:
            deps = set()
            if step.depends_on:
                for dep in step.depends_on:
                    if dep not in step_map:
                        raise WorkflowValidationError(
                            f"Step '{step.name}' depends on unknown step '{dep}'"
                        )
                    deps.add(dep)
            dependencies[step.name] = deps
        return dependencies

    @classmethod
    def _topological_sort(
        cls,
        workflow: Workflow,
        step_map: Dict[str, Step],
        dependencies: Dict[str, Set[str]]
    ) -> List[Step]:
        """Topological sort to determine execution order."""
        # Count incoming edges
        in_degree = {name: 0 for name in step_map}
        for deps in dependencies.values():
            for dep in deps:
                in_degree[dep] = in_degree.get(dep, 0) + 1

        # Queue for steps with no dependencies
        queue = deque([name for name, degree in in_degree.items() if degree == 0])

        ordered = []
        while queue:
            name = queue.popleft()
            ordered.append(step_map[name])

            # Reduce in-degree of dependents
            for step_name, deps in dependencies.items():
                if name in deps:
                    in_degree[step_name] -= 1
                    if in_degree[step_name] == 0:
                        queue.append(step_name)

        # Check for circular dependencies
        if len(ordered) != len(step_map):
            remaining = set(step_map.keys()) - {s.name for s in ordered}
            raise WorkflowValidationError(
                f"Circular dependency detected in workflow '{workflow.name}'. "
                f"Remaining steps: {remaining}"
            )

        return ordered
