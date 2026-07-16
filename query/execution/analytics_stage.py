"""
===============================================================================
Module: query.execution.analytics_stage

Analytics execution stage – thin orchestrator.
===============================================================================
"""

from __future__ import annotations

from services.analytics import AnalyticsService

from .context_keys import ContextKeys
from .contracts import StageResult
from .execution_context import ExecutionContext
from .stage import ExecutionStage
from query.query_request import QueryRequest


class AnalyticsStage(ExecutionStage):
    def __init__(self, service: AnalyticsService) -> None:
        self._service = service

    @property
    def name(self) -> str:
        return "analytics"

    def execute(
        self,
        request: QueryRequest,
        context: ExecutionContext,
    ) -> StageResult:
        analytics = self._service.analyze(request, context)
        context.set(ContextKeys.ANALYTICS_RESULT, analytics)
        return StageResult(
            success=True,
            stage=self.name,
        )
