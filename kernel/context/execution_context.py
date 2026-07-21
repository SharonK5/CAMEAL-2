# kernel/context/execution_context.py
"""
Execution context – overall runtime state.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict
from uuid import UUID, uuid4

from .request_context import RequestContext
from .security_context import SecurityContext
from .workflow_context import WorkflowContext
from .trace_context import TraceContext
from .provenance_context import ProvenanceContext
from .exceptions import ContextValidationError


@dataclass(frozen=True)
class ExecutionContext:
    """
    Immutable execution context for a request.

    Attributes:
        execution_id: Unique execution identifier.
        request: Request context.
        security: Security context.
        workflow: Workflow context.
        trace: Trace context.
        provenance: Provenance context.
        created_at: Timestamp of context creation.
        updated_at: Timestamp of last update.
        metadata: Additional execution metadata.
    """

    execution_id: UUID = field(default_factory=uuid4)
    request: RequestContext = field(default_factory=RequestContext)
    security: SecurityContext = field(default_factory=SecurityContext)
    workflow: WorkflowContext = field(default_factory=WorkflowContext)
    trace: TraceContext = field(default_factory=TraceContext)
    provenance: ProvenanceContext = field(default_factory=ProvenanceContext)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

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
            security=kwargs.get("security", self.security),
            workflow=kwargs.get("workflow", self.workflow),
            trace=kwargs.get("trace", self.trace),
            provenance=kwargs.get("provenance", self.provenance),
            created_at=self.created_at,
            updated_at=datetime.now(timezone.utc),
            metadata={**self.metadata, **kwargs.get("metadata", {})},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": str(self.execution_id),
            "request": self.request.to_dict(),
            "security": self.security.to_dict(),
            "workflow": self.workflow.to_dict(),
            "trace": self.trace.to_dict(),
            "provenance": self.provenance.to_dict(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
        }	
