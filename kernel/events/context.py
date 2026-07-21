# kernel/events/context.py
"""
Event execution context.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Any, Dict
from uuid import UUID, uuid4


@dataclass(frozen=True)
class EventContext:
    """
    Immutable execution context for events.

    Carries metadata through the event processing pipeline.
    """

    request_id: UUID = field(default_factory=uuid4)
    correlation_id: Optional[str] = None
    workflow_id: Optional[str] = None
    session_id: Optional[str] = None
    identity: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    trace_id: Optional[str] = None
    parent_event_id: Optional[str] = None
    provenance: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.timestamp.tzinfo is None:
            object.__setattr__(self, "timestamp", self.timestamp.replace(tzinfo=timezone.utc))

    def with_metadata(self, **kwargs) -> "EventContext":
        """Create a new context with additional metadata."""
        new_metadata = {**self.metadata, **kwargs}
        return EventContext(
            request_id=self.request_id,
            correlation_id=self.correlation_id,
            workflow_id=self.workflow_id,
            session_id=self.session_id,
            identity=self.identity,
            timestamp=self.timestamp,
            trace_id=self.trace_id,
            parent_event_id=self.parent_event_id,
            provenance=self.provenance,
            metadata=new_metadata,
        )
