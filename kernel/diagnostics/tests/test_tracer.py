import pytest
from kernel.diagnostics.base.tracer import Tracer


def test_trace_event():
    tracer = Tracer(trace_limit=2)
    event = type("Event", (), {"event_type": "workflow.started", "payload": {"workflow": "test"}})()
    tracer.record(event)
    traces = tracer.get_traces()
    assert len(traces) == 1
    assert traces[0]["type"] == "workflow.started"
    assert traces[0]["workflow"] == "test"


def test_trace_limit():
    tracer = Tracer(trace_limit=2)
    for i in range(5):
        tracer.record(type("Event", (), {"event_type": "workflow.started", "payload": {"id": i}})())
    traces = tracer.get_traces()
    assert len(traces) == 2
    assert traces[0]["id"] == 3
    assert traces[1]["id"] == 4


def test_clear():
    tracer = Tracer()
    tracer.record(type("Event", (), {"event_type": "workflow.started"})())
    assert len(tracer.get_traces()) == 1
    tracer.clear()
    assert len(tracer.get_traces()) == 0
