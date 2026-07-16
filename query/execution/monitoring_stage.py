"""
===============================================================================
Module: query.execution.monitoring_stage

Monitoring execution stage – thin orchestrator.
===============================================================================
"""

from __future__ import annotations

from services.monitoring import MonitoringService

from .context_keys import ContextKeys
from .contracts import StageResult
from .execution_context import ExecutionContext
from .stage import ExecutionStage
from query.query_request import QueryRequest


class MonitoringStage(ExecutionStage):
    def __init__(self, service: MonitoringService) -> None:
        self._service = service

    @property
    def name(self) -> str:
        return "monitoring"

    def execute(
        self,
        request: QueryRequest,
        context: ExecutionContext,
    ) -> StageResult:
        monitoring = self._service.monitor(request, context)
        context.set(ContextKeys.MONITORING_RESULT, monitoring)
        return StageResult(
            success=True,
            stage=self.name,
        )
