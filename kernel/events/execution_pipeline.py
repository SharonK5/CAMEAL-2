# kernel/events/execution_pipeline.py
"""
Execution pipeline for event processing.
"""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Optional, Union

from .event_envelope import EventEnvelope, EventStatus
from .subscriber import AsyncSubscriber
from .exceptions import EventDispatchError

logger = logging.getLogger(__name__)


class ExecutionPipeline:
    """
    Ordered execution of event subscribers.

    Supports both synchronous and asynchronous subscribers.
    """

    def __init__(self, max_workers: int = 4) -> None:
        self._steps: List[Callable] = []
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._loop = asyncio.new_event_loop()

    def add_step(self, step: Callable) -> None:
        """Add an execution step."""
        if not callable(step):
            raise ValueError("Step must be callable")
        self._steps.append(step)

    def execute(self, envelope: EventEnvelope, mode: str = "synchronous") -> EventEnvelope:
        """
        Execute the pipeline.

        Args:
            envelope: The event envelope to process.
            mode: "synchronous" (default) or "asynchronous".

        Returns:
            The updated event envelope.
        """
        envelope = envelope.with_status(EventStatus.PROCESSING)
        try:
            if mode == "asynchronous":
                self._run_async(envelope)
                return envelope.with_status(EventStatus.COMPLETED)
            else:
                return self._run_sync(envelope)
        except Exception as e:
            return envelope.with_status(EventStatus.FAILED, error=str(e))

    def _run_sync(self, envelope: EventEnvelope) -> EventEnvelope:
        for step in self._steps:
            envelope = step(envelope)
        return envelope.with_status(EventStatus.COMPLETED)

    def _run_async(self, envelope: EventEnvelope) -> None:
        for step in self._steps:
            if isinstance(step, AsyncSubscriber):
                self._executor.submit(self._safe_run_async, step, envelope)
            else:
                step(envelope)

    def _safe_run_async(self, subscriber: AsyncSubscriber, envelope: EventEnvelope) -> None:
        try:
            asyncio.run_coroutine_threadsafe(subscriber.handle_async(envelope.event), self._loop)
        except Exception as e:
            logger.error(f"Async subscriber error: {e}")
