"""
===============================================================================
Execution Stage Resolver.

Determines the ordered list of stages to execute.
===============================================================================
"""

from __future__ import annotations

from typing import Sequence

from query.query_request import QueryRequest
from .execution_context import ExecutionContext
from .execution_stage_registry import ReadOnlyExecutionStageRegistry
from .stage import ExecutionStage


class ExecutionStageResolver:
    """
    Resolves the execution order of stages for a given request and context.

    By default, returns all registered stages in registration order.
    """

    def __init__(self, registry: ReadOnlyExecutionStageRegistry) -> None:
        self._registry = registry

    def resolve(
        self,
        request: QueryRequest,
        context: ExecutionContext,
    ) -> Sequence[ExecutionStage]:
        """
        Return an ordered sequence of stages.

        Subclasses may override to implement dynamic ordering.
        """
        return self._registry.stages()
