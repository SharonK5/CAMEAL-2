# kernel/models/execution_context.py
"""
Execution context – shared state flowing through the pipeline.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4


@dataclass(frozen=True)
class ExecutionContext:
    """
    Immutable execution context for a request.

    Attributes:
        execution_id: Unique execution identifier.
        request: Original request.
        security_decision: Security outcome.
        context_data: Additional context data.
        repository_data: Data from repositories.
        evidence: Retrieved evidence.
        reasoning_output: Reasoning engine output.
        llm_outputs: LLM responses.
        ml_outputs: ML predictions.
        monitoring_metrics: Monitoring data.
        evaluation_output: Evaluation result.
        accountability_record: Accountability record.
        learning_update: Learning update data.
        metadata: Additional metadata.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    execution_id: UUID = field(default_factory=uuid4)
    request: Optional[Any] = None
    security_decision: Optional[Any] = None
    context_data: Dict[str, Any] = field(default_factory=dict)
    repository_data: Dict[str, Any] = field(default_factory=dict)
    evidence: List[Any] = field(default_factory=list)
    reasoning_output: Optional[Any] = None
    llm_outputs: Dict[str, Any] = field(default_factory=dict)
    ml_outputs: Dict[str, Any] = field(default_factory=dict)
    monitoring_metrics: Dict[str, Any] = field(default_factory=dict)
    evaluation_output: Optional[Any] = None
    accountability_record: Optional[Any] = None
    learning_update: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if self.created_at.tzinfo is None:
            object.__setattr__(self, "created_at", self.created_at.replace(tzinfo=timezone.utc))
        if self.updated_at.tzinfo is None:
            object.__setattr__(self, "updated_at", self.updated_at.replace(tzinfo=timezone.utc))

    def update(self, **kwargs) -> "ExecutionContext":
        """Create a new context with updated fields."""
        return ExecutionContext(
            execution_id=self.execution_id,
            request=kwargs.get("request", self.request),
            security_decision=kwargs.get("security_decision", self.security_decision),
            context_data={**self.context_data, **kwargs.get("context_data", {})},
            repository_data={**self.repository_data, **kwargs.get("repository_data", {})},
            evidence=self.evidence + kwargs.get("evidence", []),
            reasoning_output=kwargs.get("reasoning_output", self.reasoning_output),
            llm_outputs={**self.llm_outputs, **kwargs.get("llm_outputs", {})},
            ml_outputs={**self.ml_outputs, **kwargs.get("ml_outputs", {})},
            monitoring_metrics={**self.monitoring_metrics, **kwargs.get("monitoring_metrics", {})},
            evaluation_output=kwargs.get("evaluation_output", self.evaluation_output),
            accountability_record=kwargs.get("accountability_record", self.accountability_record),
            learning_update=kwargs.get("learning_update", self.learning_update),
            metadata={**self.metadata, **kwargs.get("metadata", {})},
            created_at=self.created_at,
            updated_at=datetime.now(timezone.utc),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": str(self.execution_id),
            "request": self.request.to_dict() if self.request and hasattr(self.request, "to_dict") else str(self.request),
            "security_decision": str(self.security_decision) if self.security_decision else None,
            "context_data": self.context_data,
            "repository_data": self.repository_data,
            "evidence": self.evidence,
            "reasoning_output": str(self.reasoning_output) if self.reasoning_output else None,
            "llm_outputs": self.llm_outputs,
            "ml_outputs": self.ml_outputs,
            "monitoring_metrics": self.monitoring_metrics,
            "evaluation_output": str(self.evaluation_output) if self.evaluation_output else None,
            "accountability_record": str(self.accountability_record) if self.accountability_record else None,
            "learning_update": str(self.learning_update) if self.learning_update else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
