# kernel/events/event_bus.py
"""
Main event bus implementation.
"""

import logging
from threading import RLock
from typing import Any, Callable, Dict, List, Optional, Type, Union

from .event import Event
from .event_envelope import EventEnvelope, EventStatus
from .dispatcher import Dispatcher
from .registry import Registry
from .validator import EventValidator
from .diagnostics import Diagnostics
from .exceptions import EventBusError, EventValidationError

logger = logging.getLogger(__name__)


class EventBus:
    """
    Publish/subscribe event bus.
    """

    def __init__(self) -> None:
        self._registry = Registry()
        self._dispatcher = Dispatcher(self._registry)
        self._validator = EventValidator()
        self._diagnostics = Diagnostics()
        self._middleware: List[Callable] = []
        self._lock = RLock()

    def register_middleware(self, middleware: Callable) -> None:
        with self._lock:
            self._middleware.append(middleware)

    def subscribe(self, event_type: str, handler: Callable, **kwargs) -> None:
        self._registry.subscribe(event_type, handler, **kwargs)

    def unsubscribe(self, subscription_id: str) -> bool:
        return self._registry.unsubscribe(subscription_id)

    def publish(self, event: Event, mode: str = "synchronous") -> None:
        with self._lock:
            envelope = EventEnvelope(event=event)
            try:
                self._validator.validate(event)
                envelope = envelope.with_status(EventStatus.DISPATCHED)

                for middleware in self._middleware:
                    envelope = middleware(envelope)

                # Dispatch and get updated envelope
                envelope = self._dispatcher.dispatch(envelope, mode)

                self._diagnostics.record_publish(event)

            except EventValidationError as e:
                self._diagnostics.record_error(event, e)
                logger.error(f"Event validation failed: {e}")
                raise

            except Exception as e:
                envelope = envelope.with_status(EventStatus.FAILED, error=str(e))
                self._diagnostics.record_error(event, e)
                logger.error(f"Event publishing failed: {e}")
                raise EventBusError(f"Failed to publish event: {e}") from e
