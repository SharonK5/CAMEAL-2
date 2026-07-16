"""
===============================================================================
Default Monitoring Service
===============================================================================
"""

from __future__ import annotations

from query.execution import MonitoringService, ExecutionContext, ContextKeys
from query.execution.contracts import MonitoringResult
from query.query_request import QueryRequest


class DefaultMonitoringService(MonitoringService):
    """
    Default implementation that collects basic metrics and checks for anomalies.
    """

    def monitor(self, request: QueryRequest, context: ExecutionContext) -> MonitoringResult:
        # Collect metrics
        repos = context.get(ContextKeys.REPOSITORIES)
        analytics = context.get(ContextKeys.ANALYTICS_RESULT)
        gov_ctx = context.get(ContextKeys.GOVERNANCE_CONTEXT)
        temporal = context.get(ContextKeys.TEMPORAL_CONTEXT)

        metrics = {
            "repos_used": len(repos) if repos else 0,
            "has_analytics": analytics is not None,
            "has_gov_context": gov_ctx is not None,
            "has_temporal": temporal is not None,
        }

        # Detect anomalies (simplified)
        anomalies = []
        if analytics and not analytics.success:
            anomalies.append("analytics_failed")
        if gov_ctx and not gov_ctx:
            anomalies.append("missing_governance_context")

        # Example temporal flag
        temporal_flags = []
        if temporal and temporal.get("invoice_delay", False):
            temporal_flags.append("invoice_approval_delay")

        return MonitoringResult(
            success=True,
            stage="monitoring",
            metrics=metrics,
            anomalies=tuple(anomalies),
            latency_ms=0.0,  # would compute in real implementation
            resource_usage={},
            stage_timings=(),
            temporal_flags=tuple(temporal_flags),
        )
