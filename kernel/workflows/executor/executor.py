# kernel/workflows/executor/executor.py
"""
Workflow executor – executes execution plans.
"""

import logging
from typing import Dict, Any, Optional

from ...context import ExecutionContext
from ...orchestrator import Orchestrator
from ...events import EventBus
from ..base.workflow import Workflow
from ..base.exceptions import WorkflowExecutionError
from .result_collector import ResultCollector

logger = logging.getLogger(__name__)


class WorkflowExecutor:
    """
    Executes a workflow via the orchestrator.
    """

    def __init__(
        self,
        orchestrator: Orchestrator,
        event_bus: Optional[EventBus] = None,
    ):
        self._orchestrator = orchestrator
        self._event_bus = event_bus
        self._result_collector = ResultCollector()

    def execute(
        self,
        workflow: Workflow,
        initial_context: Optional[ExecutionContext] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a workflow.

        Args:
            workflow: The workflow to execute.
            initial_context: Initial execution context.
            **kwargs: Additional execution parameters.

        Returns:
            A dictionary containing:
                - status: "success" or "failure"
                - results: Step results
                - errors: Step errors (if any)
                - execution_time: Total execution time

        Raises:
            WorkflowExecutionError: If execution fails.
        """
        logger.info(f"Executing workflow: {workflow.name}")

        # Create execution plan
        from ..planner.planner import WorkflowPlanner
        steps = WorkflowPlanner.plan(workflow)

        # Execute each step
        results = {}
        errors = {}
        context = initial_context or ExecutionContext()

        for step in steps:
            try:
                logger.debug(f"Executing step: {step.name} (plugin: {step.plugin})")
                # Execute the step via the orchestrator
                result = self._execute_step(step, context, **kwargs)
                results[step.name] = result

                # Update context with result
                if hasattr(result, '__dict__') and 'context' in result.__dict__:
                    context = result.context

                # Emit step completed event
                if self._event_bus:
                    self._event_bus.publish({
                        "type": "workflow.step.completed",
                        "workflow": workflow.name,
                        "step": step.name,
                        "result": result,
                    })

            except Exception as e:
                logger.error(f"Step '{step.name}' failed: {e}")
                errors[step.name] = str(e)

                # Handle failure based on step configuration
                if step.on_failure == "skip":
                    continue
                elif step.on_failure == "retry":
                    # Implement retry logic here
                    continue
                else:  # "fail"
                    raise WorkflowExecutionError(
                        f"Step '{step.name}' failed: {e}"
                    ) from e

        return self._result_collector.collect(
            workflow=workflow,
            results=results,
            errors=errors,
        )

    def _execute_step(self, step, context, **kwargs):
        """
        Execute a single step via the orchestrator.
        """
        # The orchestrator expects a request with the step name
        from ...models import Request

        request = Request(
            request_id=f"{step.name}-{id(step)}",
            workflow_name=step.plugin,
            context=context.to_dict() if hasattr(context, 'to_dict') else {},
            metadata={
                "step": step.name,
                "plugin": step.plugin,
                "config": step.config,
            },
        )

        # Execute via orchestrator
        response = self._orchestrator.execute(request)
        return {
            "status": "success",
            "response": response,
        }
