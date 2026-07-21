# kernel/events/tests/test_dispatcher.py
import pytest

from kernel.events.dispatcher import Dispatcher
from kernel.events.registry import Registry
from kernel.events.event import Event
from kernel.events.event_envelope import EventEnvelope


class TestDispatcher:
    def test_dispatch(self):
        registry = Registry()
        dispatcher = Dispatcher(registry)
        calls = []

        def handler(event):
            calls.append(event.event_type)

        registry.subscribe("test", handler)
        envelope = EventEnvelope(event=Event(event_type="test"))
        result = dispatcher.dispatch(envelope)
        assert calls == ["test"]
        # Check that results are stored
        assert result.subscriber_results is not None

    def test_priority_ordering(self):
        registry = Registry()
        dispatcher = Dispatcher(registry)
        calls = []

        def handler1(event):
            calls.append("high")

        def handler2(event):
            calls.append("low")

        registry.subscribe("test", handler1, priority=10)
        registry.subscribe("test", handler2, priority=0)
        envelope = EventEnvelope(event=Event(event_type="test"))
        dispatcher.dispatch(envelope)
        assert calls == ["high", "low"]

    def test_filter(self):
        registry = Registry()
        dispatcher = Dispatcher(registry)
        calls = []

        def handler(event):
            calls.append("called")

        registry.subscribe("test", handler, filter=lambda e: e.payload.get("pass") is True)
        envelope = EventEnvelope(event=Event(event_type="test", payload={"pass": True}))
        dispatcher.dispatch(envelope)
        assert calls == ["called"]

        calls.clear()
        envelope = EventEnvelope(event=Event(event_type="test", payload={"pass": False}))
        dispatcher.dispatch(envelope)
        assert calls == []
