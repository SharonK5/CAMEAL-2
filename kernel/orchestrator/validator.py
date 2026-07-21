# kernel/orchestrator/validator.py
"""
Internal validation component.

Validates execution plans and pipelines before execution.
"""

from typing import Optional
from ..managers import EngineManager
from .pipeline import Pipeline
from .exceptions import PlanValidationError


class Validator:
    """
    Validates execution plans and pipelines.

    Checks:
    - Pipeline is not empty.
    - All engines referenced exist in the engine manager.
    - No duplicate stages (if configured).
    - The pipeline is internally consistent.
    """

    def __init__(
        self,
        engine_manager: EngineManager,
        allow_duplicates: bool = False,
    ) -> None:
        """
        Initialize the validator.

        Args:
            engine_manager: The engine manager used to resolve engine existence.
            allow_duplicates: If True, duplicate stage names are allowed.
                Default: False (duplicates raise a validation error).
        """
        self._engine_manager = engine_manager
        self._allow_duplicates = allow_duplicates

    def validate(self, pipeline: Pipeline) -> None:
        """
        Validate the pipeline.

        Args:
            pipeline: The pipeline to validate.

        Raises:
            PlanValidationError: If any validation check fails.
        """
        if pipeline.is_empty:
            raise PlanValidationError("Pipeline is empty – at least one stage is required")

        # Check engine existence and duplicates
        seen = set()
        for stage in pipeline:
            # Check engine exists
            if not self._engine_manager.has(stage):
                raise PlanValidationError(
                    f"Engine '{stage}' is not registered"
                )

            # Check duplicates
            if not self._allow_duplicates:
                if stage in seen:
                    raise PlanValidationError(
                        f"Duplicate stage '{stage}' found in pipeline"
                    )
                seen.add(stage)

        # Optional: additional business rules (e.g., ordering constraints)
        # For example, enforce that Security must come first, etc.
        # These can be added as extensions.

    def validate_plan(self, plan) -> None:
        """
        Validate an ExecutionPlan (if you use that class).

        This is a convenience wrapper around validate().
        Converts ExecutionPlan to Pipeline if needed.
        """
        # If your ExecutionPlan has a to_pipeline() method, use it.
        # Otherwise, create a Pipeline from the plan.
        from .pipeline import Pipeline

        if hasattr(plan, 'to_pipeline'):
            pipeline = plan.to_pipeline()
        else:
            # Assume plan has workflow_name and engine_names attributes
            pipeline = Pipeline(
                workflow_name=plan.workflow_name,
                stages=tuple(plan.engine_names),
                metadata=plan.metadata,
            )
        self.validate(pipeline)
