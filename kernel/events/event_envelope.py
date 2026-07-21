# kernel/events/event_envelope.py
"""
EventEnvelope – runtime processing state for an Event.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from .event import Event


class EventStatus(str, Enum):
    CREATED = "created"
    VALIDATED = "validated"
    DISPATCHED = "dispatched"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"


@dataclass(frozen=True)
class EventEnvelope:
    event: Event
    status: EventStatus = EventStatus.CREATED
    retry_count: int = 0
    delivery_attempt: int = 0
    subscriber_results: Dict[str, Any] = field(default_factory=dict)
    processing_time_ms: float = 0.0
    dispatched_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    envelope_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if self.status == EventStatus.DISPATCHED and self.dispatched_at is None:
            object.__setattr__(self, "dispatched_at", datetime.now(timezone.utc))
        if self.status == EventStatus.COMPLETED and self.completed_at is None:
            object.__setattr__(self, "completed_at", datetime.now(timezone.utc))
        if not isinstance(self.event, Event):
            raise TypeError("event must be an Event instance")
        if self.processing_time_ms < 0:
            raise ValueError("processing_time_ms cannot be negative")
        if self.retry_count < 0:
            raise ValueError("retry_count cannot be negative")

    def with_status(self, status: EventStatus, error: Optional[str] = None) -> "EventEnvelope":
        return EventEnvelope(
            event=self.event,
            status=status,
            retry_count=self.retry_count,
            delivery_attempt=self.delivery_attempt + 1 if status != EventStatus.FAILED else self.delivery_attempt,
            subscriber_results=self.subscriber_results,
            processing_time_ms=self.processing_time_ms,
            dispatched_at=self.dispatched_at or datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc) if status == EventStatus.COMPLETED else None,
            error=error or self.error,
            envelope_id=self.envelope_id,
        )

    def with_results(self, results: Dict[str, Any]) -> "EventEnvelope":
        """Create a new envelope with updated subscriber results."""
        return EventEnvelope(
            event=self.event,
            status=self.status,
            retry_count=self.retry_count,
            delivery_attempt=self.delivery_attempt,
            subscriber_results=results,
            processing_time_ms=self.processing_time_ms,
            dispatched_at=self.dispatched_at,
            completed_at=self.completed_at,
            error=self.error,
            envelope_id=self.envelope_id,
        )

    def with_retry(self) -> "EventEnvelope":
        return EventEnvelope(
            event=self.event,
            status=EventStatus.CREATED,
            retry_count=self.retry_count + 1,
            delivery_attempt=0,
            subscriber_results={},
            processing_time_ms=0.0,
            dispatched_at=None,
            completed_at=None,
            error=None,
            envelope_id=self.envelope_id,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "envelope_id": str(self.envelope_id),
            "event": self.event.to_dict(),
            "status": self.status.value,
            "retry_count": self.retry_count,
            "delivery_attempt": self.delivery_attempt,
            "subscriber_results": self.subscriber_results,
            "processing_time_ms": self.processing_time_ms,
            "dispatched_at": self.dispatched_at.isoformat() if self.dispatched_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error": self.error,
        }
