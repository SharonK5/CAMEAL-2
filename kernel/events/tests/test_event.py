# kernel/events/tests/test_event.py
import pytest
from datetime import datetime, timezone
from uuid import UUID

from kernel.events.event import Event, EventPriority, EventCategory, EventType
from kernel.events.exceptions import EventValidationError


class TestEvent:
    def test_event_creation(self):
        event = Event(event_type=EventType.REQUEST_RECEIVED, payload={"id": "123"})
        assert event.event_type == EventType.REQUEST_RECEIVED
        assert event.payload == {"id": "123"}
        assert event.priority == EventPriority.NORMAL
        assert event.category == EventCategory.SYSTEM
        assert isinstance(event.event_id, UUID)
        assert event.timestamp.tzinfo == timezone.utc

    def test_event_validation(self):
        with pytest.raises(EventValidationError, match="Event type cannot be empty"):
            Event(event_type="")

    def test_event_eq_by_id(self):
        event1 = Event(event_type="test", event_id=UUID("12345678-1234-5678-1234-567812345678"))
        event2 = Event(event_type="test", event_id=UUID("12345678-1234-5678-1234-567812345678"))
        assert event1 == event2

    def test_event_to_dict(self):
        event = Event(
            event_type=EventType.REQUEST_RECEIVED,
            payload={"id": "123"},
            source="test_source",
            correlation_id="corr-123",
            trace_id="trace-456",
        )
        d = event.to_dict()
        assert d["event_type"] == EventType.REQUEST_RECEIVED
        assert d["payload"] == {"id": "123"}
        assert d["source"] == "test_source"
        assert d["correlation_id"] == "corr-123"
        assert d["trace_id"] == "trace-456"
        assert "event_id" in d
        assert "timestamp" in d

    def test_event_from_dict(self):
        data = {
            "event_id": "12345678-1234-5678-1234-567812345678",
            "event_type": EventType.REQUEST_RECEIVED,
            "payload": {"id": "123"},
            "schema_version": "1.0",
            "priority": "normal",
            "source": "test",
            "timestamp": "2024-01-01T00:00:00+00:00",
            "correlation_id": "corr-123",
            "trace_id": "trace-456",
            "category": "system",
            "provenance": {},
            "metadata": {},
        }
        event = Event.from_dict(data)
        assert event.event_type == EventType.REQUEST_RECEIVED
        assert event.payload == {"id": "123"}
        assert event.source == "test"
        assert event.correlation_id == "corr-123"
        assert event.trace_id == "trace-456"

    def test_event_to_json_from_json(self):
        event = Event(event_type=EventType.REQUEST_RECEIVED, payload={"id": "123"})
        json_str = event.to_json()
        event2 = Event.from_json(json_str)
        assert event == event2
