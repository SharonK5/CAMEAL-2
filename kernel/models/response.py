# kernel/models/response.py
"""
Response model – output from the kernel.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Response:
    """
    Immutable response object.

    Attributes:
        response_id: Unique response identifier.
        decision: Final decision (ALLOW, DENY, REVIEW, ESCALATE).
        evidence: Supporting evidence.
        provenance: Full trace of execution.
        metrics: Timing and performance metrics.
        execution_time_ms: Total execution time in milliseconds.
        trace: Step-by-step execution trace.
        recommendations: Suggested actions.
        error: Optional error message.
        data: Additional response data.
    """

    response_id: UUID = field(default_factory=uuid4)
    decision: str = ""
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    provenance: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    trace: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    error: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "response_id": str(self.response_id),
            "decision": self.decision,
            "evidence": self.evidence,
            "provenance": self.provenance,
            "metrics": self.metrics,
            "execution_time_ms": self.execution_time_ms,
            "trace": self.trace,
            "recommendations": self.recommendations,
            "error": self.error,
            "data": self.data,
        }
