# kernel/events/tests/test_execution_pipeline.py
import pytest

from kernel.events.execution_pipeline import ExecutionPipeline
from kernel.events.event import Event
from kernel.events.event_envelope import EventEnvelope


class TestExecutionPipeline:
    def test_synchronous_execution(self):
        pipeline = ExecutionPipeline()
        calls = []

        def step1(envelope):
            calls.append("step1")
            return envelope

        def step2(envelope):
            calls.append("step2")
            return envelope

        pipeline.add_step(step1)
        pipeline.add_step(step2)
        event = Event(event_type="test")
        envelope = EventEnvelope(event=event)
        result = pipeline.execute(envelope, mode="synchronous")
        assert result.status.value == "completed"
        assert calls == ["step1", "step2"]

    def test_asynchronous_execution(self):
        import time

        pipeline = ExecutionPipeline()
        calls = []

        def step(envelope):
            calls.append("async_step")
            return envelope

        pipeline.add_step(step)
        event = Event(event_type="test")
        envelope = EventEnvelope(event=event)
        result = pipeline.execute(envelope, mode="asynchronous")
        assert result.status.value == "completed"
        # Give time for async execution
        time.sleep(0.1)
        assert "async_step" in calls
