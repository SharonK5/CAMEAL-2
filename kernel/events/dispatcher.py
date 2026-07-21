# kernel/events/dispatcher.py
"""
Event dispatcher.
"""

import logging
from typing import Tuple

from .event_envelope import EventEnvelope, EventStatus
from .registry import Registry
from .exceptions import EventDispatchError

logger = logging.getLogger(__name__)


class Dispatcher:
    """
    Dispatches events to subscribers.
    """

    def __init__(self, registry: Registry) -> None:
        self._registry = registry

    def dispatch(self, envelope: EventEnvelope, mode: str = "synchronous") -> EventEnvelope:
        """
        Dispatch an event to all registered subscribers.

        Returns:
            The updated event envelope with subscriber results.
        """
        event = envelope.event
        subscriptions = self._registry.get_subscriptions(event.event_type)
        if not subscriptions:
            return envelope

        # Sort by priority (higher priority first)
        subscriptions.sort(key=lambda s: s.priority, reverse=True)

        results = {}
        for subscription in subscriptions:
            if not subscription.enabled:
                continue

            # Apply filter if present
            if subscription.filter and not subscription.filter(event):
                continue

            try:
                # Execute the subscriber
                subscription.handler(event)
                results[subscription.name or str(subscription.subscription_id)] = "success"
            except Exception as e:
                logger.error(f"Subscriber error: {e}")
                results[subscription.name or str(subscription.subscription_id)] = {"error": str(e)}

        # Create new envelope with results
        return envelope.with_results(results)
