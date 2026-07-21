# kernel/events/serializer.py
"""
Event serializer for persistence and transport.

Provides serialization and deserialization for Events and EventEnvelopes.
"""

import json
from typing import Any, Dict
from uuid import UUID
from datetime import datetime

from .event import Event
from .event_envelope import EventEnvelope, EventStatus
from .exceptions import EventSerializationError


class EventSerializer:
    """
    Serializes and deserializes events and envelopes.
    """

    # ------------------------------------------------------------------
    # Event Serialization
    # ------------------------------------------------------------------

    @staticmethod
    def serialize_event(event: Event) -> Dict[str, Any]:
        """Serialize an event to a dictionary."""
        return event.to_dict()

    @staticmethod
    def deserialize_event(data: Dict[str, Any]) -> Event:
        """Deserialize an event from a dictionary."""
        return Event.from_dict(data)

    @staticmethod
    def event_to_json(event: Event) -> str:
        """Serialize an event to JSON."""
        return json.dumps(EventSerializer.serialize_event(event), default=str)

    @staticmethod
    def event_from_json(data: str) -> Event:
        """Deserialize an event from JSON."""
        return EventSerializer.deserialize_event(json.loads(data))

    # ------------------------------------------------------------------
    # Envelope Serialization
    # ------------------------------------------------------------------

    @staticmethod
    def serialize_envelope(envelope: EventEnvelope) -> Dict[str, Any]:
        """Serialize an envelope to a dictionary."""
        return envelope.to_dict()

    @staticmethod
    def deserialize_envelope(data: Dict[str, Any]) -> EventEnvelope:
        """Deserialize an envelope from a dictionary."""
        try:
            return EventEnvelope(
                event=Event.from_dict(data["event"]),
                status=EventStatus(data.get("status", "created")),
                retry_count=data.get("retry_count", 0),
                delivery_attempt=data.get("delivery_attempt", 0),
                subscriber_results=data.get("subscriber_results", {}),
                processing_time_ms=data.get("processing_time_ms", 0.0),
                dispatched_at=datetime.fromisoformat(data["dispatched_at"]) if data.get("dispatched_at") else None,
                completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
                error=data.get("error"),
                envelope_id=UUID(data["envelope_id"]),
            )
        except Exception as e:
            raise EventSerializationError(f"Failed to deserialize envelope: {e}") from e

    @staticmethod
    def envelope_to_json(envelope: EventEnvelope) -> str:
        """Serialize an envelope to JSON."""
        return json.dumps(EventSerializer.serialize_envelope(envelope), default=str)

    @staticmethod
    def envelope_from_json(data: str) -> EventEnvelope:
        """Deserialize an envelope from JSON."""
        return EventSerializer.deserialize_envelope(json.loads(data))
