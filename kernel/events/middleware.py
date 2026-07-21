# kernel/events/middleware.py
"""
Event middleware.

Middleware provides cross-cutting processing hooks that execute before
and after event dispatch. Typical uses include logging, metrics, tracing,
security checks, and auditing.

Middleware functions receive an EventEnvelope and return an EventEnvelope.
"""

import time
import logging
from typing import Callable, List, Optional

from .event_envelope import EventEnvelope

logger = logging.getLogger(__name__)


class Middleware:
    """
    Middleware pipeline for cross-cutting event processing.

    Middleware functions are executed in the order they are added.
    Each function receives an EventEnvelope and must return an EventEnvelope.
    """

    def __init__(self) -> None:
        self._middleware: List[Callable[[EventEnvelope], EventEnvelope]] = []

    def add(self, middleware: Callable[[EventEnvelope], EventEnvelope]) -> None:
        """Add a middleware function."""
        if not callable(middleware):
            raise ValueError("Middleware must be callable")
        self._middleware.append(middleware)

    def process(self, envelope: EventEnvelope) -> EventEnvelope:
        """Process an event through all middleware."""
        for middleware in self._middleware:
            try:
                envelope = middleware(envelope)
            except Exception as e:
                logger.error(f"Middleware error: {e}")
                # Continue processing; middleware should not break the pipeline
        return envelope


# ------------------------------------------------------------------
# Built-in Middleware
# ------------------------------------------------------------------

def logging_middleware(envelope: EventEnvelope) -> EventEnvelope:
    """Log event publication and completion."""
    event = envelope.event
    logger.info(f"Event {event.event_type} ({event.event_id}) published from {event.source}")
    return envelope


def timing_middleware(envelope: EventEnvelope) -> EventEnvelope:
    """Measure event processing time."""
    if envelope.dispatched_at:
        elapsed = (time.time() - envelope.dispatched_at.timestamp()) * 1000
        object.__setattr__(envelope, "processing_time_ms", elapsed)
    return envelope


def tracing_middleware(envelope: EventEnvelope) -> EventEnvelope:
    """Add trace information to the envelope."""
    event = envelope.event
    if event.trace_id:
        logger.debug(f"Trace: {event.trace_id} | Event: {event.event_type}")
    return envelope


def audit_middleware(envelope: EventEnvelope) -> EventEnvelope:
    """Record audit entry for the event."""
    event = envelope.event
    logger.info(f"AUDIT: {event.event_type} | {event.event_id} | source={event.source}")
    return envelope
