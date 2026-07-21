# kernel/orchestrator/executor.py
"""
Internal execution component.

Iterates through a pipeline, invoking the dispatcher for each stage,
propagating execution context, and handling failures.
"""

import logging
from typing import Optional
from ..context import ExecutionContext
from ..events import EventBus
from .pipeline import Pipeline
from .dispatcher import Dispatcher
from .exceptions import ExecutionError


logger = logging.getLogger(__name__)


class Executor:
    """
    Executes an immutable execution pipeline.

    The executor is stateless and thread-safe.
    Each call to execute() runs a complete pipeline.

    The executor:
    - Iterates through pipeline stages in order.
    - For each stage, invokes the dispatcher with the current context.
    - Propagates the updated context to the next stage.
    - Stops on the first unrecoverable error.
    - Returns the final context on success.
    """

    def __init__(
        self,
        dispatcher: Dispatcher,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        """
        Initialize the executor.

        Args:
            dispatcher: The dispatcher used to invoke engines.
            event_bus: Optional event bus for publishing execution events.
        """
        self._dispatcher = dispatcher
        self._event_bus = event_bus

    def execute(self, pipeline: Pipeline, initial_context: ExecutionContext) -> ExecutionContext:
        """
        Execute the pipeline.

        Args:
            pipeline: The immutable pipeline to execute.
            initial_context: The starting execution context.

        Returns:
            ExecutionContext: The final context after all stages.

        Raises:
            ExecutionError: If any stage fails unrecoverably.
        """
        if pipeline.is_empty:
            logger.warning("Executing empty pipeline – returning initial context unchanged")
            return initial_context

        context = initial_context

        for stage in pipeline:
            logger.debug(f"Executing stage: {stage}")

            try:
                # Invoke the engine via dispatcher
                context = self._dispatcher.dispatch(stage, context)

                # Publish stage completion event (optional)
                if self._event_bus:
                    self._event_bus.publish(
                        self._create_stage_event(stage, context, success=True)
                    )

            except Exception as e:
                logger.error(f"Stage '{stage}' failed: {e}")

                # Publish failure event (optional)
                if self._event_bus:
                    self._event_bus.publish(
                        self._create_stage_event(stage, context, success=False, error=e)
                    )

                # Re-raise as execution error
                raise ExecutionError(
                    f"Execution failed at stage '{stage}': {e}"
                ) from e

        logger.info(f"Pipeline '{pipeline.workflow_name}' completed successfully")
        return context

    def _create_stage_event(self, stage: str, context: ExecutionContext, success: bool, error: Optional[Exception] = None):
        """
        Create a stage execution event.
        This is a placeholder; you can define specific event classes later.
        """
        # For simplicity, return a dict; you might want to use a typed event class.
        return {
            "type": "engine.stage.executed",
            "stage": stage,
            "success": success,
            "request_id": context.get("request_id"),
            "error": str(error) if error else None,
        }
