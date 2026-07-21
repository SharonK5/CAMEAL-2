# kernel/events/tests/test_filters.py
import pytest

from kernel.events.filters import EventFilter
from kernel.events.event import Event


class TestFilters:
    def test_by_type(self):
        f = EventFilter.by_type("test")
        event = Event(event_type="test")
        assert f(event) is True
        event2 = Event(event_type="other")
        assert f(event2) is False

    def test_by_source(self):
        f = EventFilter.by_source("src")
        event = Event(event_type="test", source="src")
        assert f(event) is True

    def test_by_payload_field(self):
        f = EventFilter.by_payload_field("key", "value")
        event = Event(event_type="test", payload={"key": "value"})
        assert f(event) is True

    def test_combine(self):
        f1 = EventFilter.by_type("test")
        f2 = EventFilter.by_source("src")
        combined = EventFilter.combine(f1, f2)
        event = Event(event_type="test", source="src")
        assert combined(event) is True
        event2 = Event(event_type="test", source="other")
        assert combined(event2) is False
