"""
===============================================================================
Module: query.execution.context_stage

Resolves GovernanceContext for execution.
===============================================================================
"""

from __future__ import annotations

from context.context_resolver import ContextResolver

from .context_keys import ContextKeys
from .contracts import StageResult
from .execution_context import ExecutionContext
from .stage import ExecutionStage


class ContextStage(ExecutionStage):
    """
    Resolves the governance context associated with a query.
    """

    def __init__(self, resolver: ContextResolver) -> None:
        self._resolver = resolver

    @property
    def name(self) -> str:
        return "context"

    def execute(
        self,
        request,
        context: ExecutionContext,
    ) -> StageResult:
        # If a context is already attached to the request, use it.
        if request.context is not None:
            gov_context = request.context
        else:
            # Otherwise, resolve it using the resolver.
            gov_context = self._resolver.resolve(request)

        context.set(ContextKeys.GOVERNANCE_CONTEXT, gov_context)
        return StageResult(
            success=True,
            stage=self.name,
            metadata=(("resolved", gov_context is not None),),
        )
