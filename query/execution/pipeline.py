"""
===============================================================================
Module: query.execution.pipeline

Ordered execution pipeline.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

import warnings

from query.query_request import QueryRequest
from query.query_response import QueryResponse

from .execution_context import ExecutionContext
from .exceptions import DuplicateStageError
from .stage import ExecutionStage


class ExecutionPipeline:
    """
    Ordered execution pipeline.
    """

    def __init__(self) -> None:

        self._stages: list[ExecutionStage] = []

    # ------------------------------------------------------------------

    @property
    def stages(self) -> tuple[ExecutionStage, ...]:

        return tuple(self._stages)

    # ------------------------------------------------------------------

    def add_stage(
        self,
        stage: ExecutionStage,
    ) -> None:

        if any(s.name == stage.name for s in self._stages):
            raise DuplicateStageError(
                f"Stage '{stage.name}' already exists."
            )

        self._stages.append(stage)

    # ------------------------------------------------------------------

    def remove_stage(
        self,
        name: str,
    ) -> None:

        self._stages = [
            stage
            for stage in self._stages
            if stage.name != name
        ]

    # ------------------------------------------------------------------

    def clear(self) -> None:

        self._stages.clear()

    # ------------------------------------------------------------------

    def execute(
        self,
        request: QueryRequest,
        context: ExecutionContext | None = None,
    ) -> QueryResponse | None:
        """
        Execute every stage.

        A stage may terminate execution by returning
        a QueryResponse.

        If no context is provided, a new one is created
        for backward compatibility. This fallback will
        be removed in a future release – callers should
        pass an explicit ExecutionContext.
        """

        if context is None:
            warnings.warn(
                "Creating ExecutionContext internally is deprecated. "
                "Pass one explicitly to pipeline.execute().",
                DeprecationWarning,
                stacklevel=2,
            )
            context = ExecutionContext()

        for stage in self._stages:

            response = stage.execute(
                request,
                context,
            )

            if response is not None:
                return response

        return None

# Compatibility alias
Pipeline = ExecutionPipeline
