# kernel/events/publisher.py
"""
Event publisher abstraction.
"""

from typing import Any, Dict, Optional
from uuid import uuid4

from .event import Event, EventPriority, EventCategory
from .event_bus import EventBus


class Publisher:
    """
    Event publisher helper.

    Provides a convenient interface for publishing events.
    """

    def __init__(self, event_bus: EventBus, source: Optional[str] = None) -> None:
        self._event_bus = event_bus
        self._source = source

    def publish(
        self,
        event_type: str,
        payload: Optional[Dict[str, Any]] = None,
        priority: EventPriority = EventPriority.NORMAL,
        correlation_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        category: EventCategory = EventCategory.SYSTEM,
        provenance: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        mode: str = "synchronous",
    ) -> Event:
        """
        Create and publish an event.
        """
        event = Event(
            event_type=event_type,
            payload=payload or {},
            priority=priority,
            source=self._source,
            correlation_id=correlation_id,
            trace_id=trace_id,
            category=category,
            provenance=provenance or {},
            metadata=metadata or {},
        )
        self._event_bus.publish(event, mode)
        return event
