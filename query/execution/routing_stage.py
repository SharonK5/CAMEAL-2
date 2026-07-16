"""
===============================================================================
Module: query.execution.routing_stage
===============================================================================
"""

from __future__ import annotations

from query.query_router import QueryRouter

from .context_keys import ContextKeys
from .contracts import RoutingResult
from .execution_context import ExecutionContext
from .stage import ExecutionStage


class RoutingStage(ExecutionStage):
    def __init__(self, router: QueryRouter) -> None:
        self._router = router

    @property
    def name(self) -> str:
        return "routing"

    def execute(
        self,
        request,
        context: ExecutionContext,
    ) -> RoutingResult:
        handler = self._router.handler(request.intent)

        if handler is None:
            raise KeyError(f"No handler for '{request.intent.name}'.")

        context.set(ContextKeys.QUERY_HANDLER, handler)

        return RoutingResult(
            success=True,
            stage=self.name,
            handler=handler,
            handler_name=handler.__class__.__name__,
            metadata=(("resolved", True),),
        )
