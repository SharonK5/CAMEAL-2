# kernel/events/event.py
"""
Immutable event contract for the CAMEAL Kernel.

An Event represents a fact that occurred. It is immutable, serializable,
versioned, thread-safe, transportable, and plugin-safe.

Processing state (status, retries, delivery attempts) belongs to the
EventEnvelope, not to the Event itself.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Dict, Optional, Union
from uuid import UUID, uuid4

from .exceptions import EventValidationError


class EventPriority(str, Enum):
    """Priority levels for event ordering."""

    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
    BACKGROUND = "background"

    def __lt__(self, other: "EventPriority") -> bool:
        order = [
            EventPriority.CRITICAL,
            EventPriority.HIGH,
            EventPriority.NORMAL,
            EventPriority.LOW,
            EventPriority.BACKGROUND,
        ]
        return order.index(self) < order.index(other)


class EventCategory(str, Enum):
    """High-level categories for event grouping and filtering."""

    SYSTEM = "system"
    SECURITY = "security"
    WORKFLOW = "workflow"
    REPOSITORY = "repository"
    REASONING = "reasoning"
    MONITORING = "monitoring"
    EVALUATION = "evaluation"
    ACCOUNTABILITY = "accountability"
    LEARNING = "learning"
    ADAPTATION = "adaptation"
    RESPONSE = "response"
    DIAGNOSTICS = "diagnostics"


# Standard event type catalog
class EventType:
    """Catalog of standard kernel event types."""

    # System
    KERNEL_INITIALIZING = "KernelInitializing"
    KERNEL_INITIALIZED = "KernelInitialized"
    KERNEL_STARTING = "KernelStarting"
    KERNEL_STARTED = "KernelStarted"
    KERNEL_STOPPING = "KernelStopping"
    KERNEL_STOPPED = "KernelStopped"
    KERNEL_HEALTH_CHANGED = "KernelHealthChanged"

    # Request
    REQUEST_RECEIVED = "RequestReceived"
    CONTEXT_CREATED = "ContextCreated"
    EXECUTION_STARTED = "ExecutionStarted"
    EXECUTION_COMPLETED = "ExecutionCompleted"
    EXECUTION_FAILED = "ExecutionFailed"

    # Workflow
    WORKFLOW_SELECTED = "WorkflowSelected"
    WORKFLOW_STARTED = "WorkflowStarted"
    WORKFLOW_COMPLETED = "WorkflowCompleted"
    WORKFLOW_FAILED = "WorkflowFailed"

    # Security
    SECURITY_STARTED = "SecurityStarted"
    SECURITY_COMPLETED = "SecurityCompleted"
    SECURITY_DENIED = "SecurityDenied"
    AUTHENTICATION_COMPLETED = "AuthenticationCompleted"
    AUTHORIZATION_COMPLETED = "AuthorizationCompleted"
    POLICY_EVALUATED = "PolicyEvaluated"

    # Retrieval
    RETRIEVAL_STARTED = "RetrievalStarted"
    RETRIEVAL_COMPLETED = "RetrievalCompleted"
    RETRIEVAL_FAILED = "RetrievalFailed"

    # Reasoning
    REASONING_STARTED = "ReasoningStarted"
    REASONING_COMPLETED = "ReasoningCompleted"
    REASONING_FAILED = "ReasoningFailed"

    # Monitoring
    MONITORING_STARTED = "MonitoringStarted"
    MONITORING_COMPLETED = "MonitoringCompleted"

    # Evaluation
    EVALUATION_STARTED = "EvaluationStarted"
    EVALUATION_COMPLETED = "EvaluationCompleted"

    # Accountability
    ACCOUNTABILITY_STARTED = "AccountabilityStarted"
    ACCOUNTABILITY_COMPLETED = "AccountabilityCompleted"

    # Learning
    LEARNING_STARTED = "LearningStarted"
    LEARNING_COMPLETED = "LearningCompleted"

    # Adaptation
    ADAPTATION_STARTED = "AdaptationStarted"
    ADAPTATION_COMPLETED = "AdaptationCompleted"

    # Response
    RESPONSE_BUILT = "ResponseBuilt"
    RESPONSE_SENT = "ResponseSent"
    REQUEST_COMPLETED = "RequestCompleted"

    # Diagnostics
    METRIC_RECORDED = "MetricRecorded"
    TRACE_RECORDED = "TraceRecorded"
    AUDIT_RECORDED = "AuditRecorded"
    HEALTH_CHANGED = "HealthChanged"


@dataclass(frozen=True)
class Event:
    """
    Immutable event contract.

    An Event is a fact that occurred. It is not aware of its processing state.

    Attributes:
        event_id: Unique event identifier.
        event_type: String identifier for the event type (use EventType constants).
        schema_version: Version of the event schema (for evolution).
        payload: Event data payload.
        priority: Execution priority.
        source: Optional source component name.
        timestamp: Creation timestamp.
        correlation_id: Optional correlation ID (single workflow).
        trace_id: Optional trace ID (whole request chain).
        category: High-level event category.
        provenance: Optional provenance metadata (e.g., evidence IDs, models).
        metadata: Additional immutable metadata.
    """

    event_type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    event_id: UUID = field(default_factory=uuid4)
    schema_version: str = "1.0"
    priority: EventPriority = EventPriority.NORMAL
    source: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: Optional[str] = None
    trace_id: Optional[str] = None
    category: EventCategory = EventCategory.SYSTEM
    provenance: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.event_type:
            raise EventValidationError("Event type cannot be empty")
        if not isinstance(self.payload, dict):
            raise EventValidationError("Event payload must be a dictionary")
        if not isinstance(self.metadata, dict):
            raise EventValidationError("Event metadata must be a dictionary")
        if not isinstance(self.provenance, dict):
            raise EventValidationError("Event provenance must be a dictionary")
        if self.timestamp.tzinfo is None:
            object.__setattr__(self, "timestamp", self.timestamp.replace(tzinfo=timezone.utc))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Event):
            return NotImplemented
        return self.event_id == other.event_id

    def __hash__(self) -> int:
        return hash(self.event_id)

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to a dictionary."""
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "schema_version": self.schema_version,
            "payload": self.payload,
            "priority": self.priority.value,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
            "trace_id": self.trace_id,
            "category": self.category.value,
            "provenance": self.provenance,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """Reconstruct an event from a dictionary."""
        try:
            return cls(
                event_id=UUID(data["event_id"]),
                event_type=data["event_type"],
                schema_version=data.get("schema_version", "1.0"),
                payload=data.get("payload", {}),
                priority=EventPriority(data.get("priority", "normal")),
                source=data.get("source"),
                timestamp=datetime.fromisoformat(data["timestamp"]),
                correlation_id=data.get("correlation_id"),
                trace_id=data.get("trace_id"),
                category=EventCategory(data.get("category", "system")),
                provenance=data.get("provenance", {}),
                metadata=data.get("metadata", {}),
            )
        except Exception as e:
            raise EventValidationError(f"Failed to deserialize event: {e}") from e

    def to_json(self) -> str:
        """Serialize event to JSON."""
        import json
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_json(cls, data: str) -> "Event":
        """Deserialize event from JSON."""
        import json
        return cls.from_dict(json.loads(data))

    def with_metadata(self, **kwargs) -> "Event":
        """Create a new event with additional metadata."""
        new_metadata = {**self.metadata, **kwargs}
        return Event(
            event_id=self.event_id,
            event_type=self.event_type,
            schema_version=self.schema_version,
            payload=self.payload,
            priority=self.priority,
            source=self.source,
            timestamp=self.timestamp,
            correlation_id=self.correlation_id,
            trace_id=self.trace_id,
            category=self.category,
            provenance=self.provenance,
            metadata=new_metadata,
        )
