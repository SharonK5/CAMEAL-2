# kernel/workflows/executor/result_collector.py
"""
Result collector for workflow execution.
"""

from typing import Dict, Any

from ..base.workflow import Workflow


class ResultCollector:
    """
    Collects and aggregates results from workflow execution.
    """

    def collect(
        self,
        workflow: Workflow,
        results: Dict[str, Any],
        errors: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Collect results and errors into a consolidated response.

        Args:
            workflow: The workflow being executed.
            results: Results from successful steps.
            errors: Errors from failed steps.

        Returns:
            A dict containing:
                - status: "success" or "partial" or "failure"
                - workflow: workflow name
                - results: step results
                - errors: step errors
                - summary: summary statistics
        """
        total_steps = len(workflow.steps)
        success_count = len(results)
        failure_count = len(errors)

        if failure_count == 0:
            status = "success"
        elif success_count > 0:
            status = "partial"
        else:
            status = "failure"

        return {
            "status": status,
            "workflow": workflow.name,
            "results": results,
            "errors": errors,
            "summary": {
                "total_steps": total_steps,
                "successful": success_count,
                "failed": failure_count,
            }
        }
