"""
kernel.event_bus
================

Thread-safe publish/subscribe event bus for the CAMEAL Kernel.

The Event Bus enables loose coupling between system modules.
Publishers emit events without knowing who consumes them, while
subscribers register handlers for specific event types.

Responsibilities
----------------
- Subscribe handlers to events
- Publish events
- Unsubscribe handlers
- Maintain lightweight event statistics
- Provide health information

The Event Bus intentionally does not persist events. Persistent
audit trails belong to the Governance and Storage modules.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from collections.abc import Callable
from threading import RLock
from typing import Any

logger = logging.getLogger(__name__)

EventHandler = Callable[[dict[str, Any]], None]


class EventBus:
    """
    Thread-safe publish/subscribe event bus.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._subscribers: defaultdict[str, list[EventHandler]] = defaultdict(list)
        self._published_events = 0

    def subscribe(self, event: str, handler: EventHandler) -> None:
        """
        Register a handler for an event.

        Parameters
        ----------
        event
            Event name.

        handler
            Callable receiving the event payload.
        """
        with self._lock:
            if handler not in self._subscribers[event]:
                self._subscribers[event].append(handler)
                logger.info(
                    "Subscribed handler '%s' to event '%s'.",
                    handler.__name__,
                    event,
                )

    def unsubscribe(self, event: str, handler: EventHandler) -> None:
        """
        Remove a handler from an event.
        """
        with self._lock:
            if handler in self._subscribers[event]:
                self._subscribers[event].remove(handler)

                logger.info(
                    "Unsubscribed handler '%s' from event '%s'.",
                    handler.__name__,
                    event,
                )

    def publish(self, event: str, payload: dict[str, Any]) -> None:
        """
        Publish an event.

        Parameters
        ----------
        event
            Event name.

        payload
            Event payload.
        """
        with self._lock:
            handlers = list(self._subscribers.get(event, []))

        logger.debug(
            "Publishing event '%s' to %d handlers.",
            event,
            len(handlers),
        )

        for handler in handlers:
            try:
                handler(payload)

            except Exception:
                logger.exception(
                    "Handler '%s' failed while processing '%s'.",
                    handler.__name__,
                    event,
                )

        self._published_events += 1

    def subscribers(self, event: str) -> list[str]:
        """
        Return subscriber names.
        """
        with self._lock:
            return [
                handler.__name__
                for handler in self._subscribers.get(event, [])
            ]

    def clear(self) -> None:
        """
        Remove all subscriptions.
        """
        with self._lock:
            self._subscribers.clear()
            self._published_events = 0

        logger.info("Event Bus cleared.")

    def health(self) -> dict[str, Any]:
        """
        Return Event Bus health.
        """
        with self._lock:
            return {
                "status": "healthy",
                "registered_events": len(self._subscribers),
                "published_events": self._published_events,
            }


event_bus = EventBus()
