# kernel/events/registry.py
"""
Subscriber registry.
"""

from typing import Dict, List, Optional, Callable
from threading import RLock

from .subscription import Subscription
from .exceptions import EventSubscriptionError


class Registry:
    """
    Registry of event subscriptions.
    """

    def __init__(self) -> None:
        self._subscriptions: Dict[str, List[Subscription]] = {}
        self._lock = RLock()

    def subscribe(self, event_type: str, handler: Callable, **kwargs) -> None:
        """
        Register a subscription.
        """
        with self._lock:
            subscription = Subscription(
                event_type=event_type,
                handler=handler,
                priority=kwargs.get("priority", 0),
                filter=kwargs.get("filter"),
                name=kwargs.get("name"),
                enabled=kwargs.get("enabled", True),
            )
            self._subscriptions.setdefault(event_type, []).append(subscription)

    def unsubscribe(self, subscription_id: str) -> bool:
        """Remove a subscription."""
        with self._lock:
            for event_type, subs in self._subscriptions.items():
                for i, sub in enumerate(subs):
                    if str(sub.subscription_id) == subscription_id:
                        subs.pop(i)
                        if not subs:
                            del self._subscriptions[event_type]
                        return True
            return False

    def get_subscriptions(self, event_type: str) -> List[Subscription]:
        """Get all subscriptions for an event type."""
        with self._lock:
            return self._subscriptions.get(event_type, []).copy()

    def clear(self) -> None:
        """Clear all subscriptions."""
        with self._lock:
            self._subscriptions.clear()
