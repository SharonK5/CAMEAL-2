# kernel/workflows/lifecycle/workflow_lifecycle.py
"""
Workflow lifecycle management.
"""

from typing import Dict

from ...lifecycle import HealthStatus
from ..registry.workflow_registry import WorkflowRegistry


class WorkflowLifecycle:
    """
    Manages the lifecycle of all registered workflows.
    """

    @staticmethod
    def health_all(registry: WorkflowRegistry) -> Dict[str, HealthStatus]:
        """
        Return health status for all workflows.

        Returns:
            A dictionary mapping workflow name to HealthStatus.
        """
        result = {}
        for workflow in registry.all():
            try:
                # Workflows are stateless, so they're always healthy
                result[workflow.name] = HealthStatus.HEALTHY
            except Exception:
                result[workflow.name] = HealthStatus.UNHEALTHY
        return result
