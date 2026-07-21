# kernel/events/subscriber.py
"""
Subscriber abstractions for the CAMEAL Kernel Events subsystem.

Provides both synchronous and asynchronous subscriber base classes.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from .event import Event


class Subscriber(ABC):
    """
    Abstract base for synchronous event subscribers.

    Subscribers receive immutable Events and should never modify them.
    Subscribers should be stateless whenever possible.
    """

    @abstractmethod
    def handle(self, event: Event) -> None:
        """
        Handle an event.

        Args:
            event: The immutable event to process.
        """
        pass


class AsyncSubscriber(ABC):
    """
    Abstract base for asynchronous event subscribers.

    Asynchronous subscribers are executed in the background and
    do not block the main execution pipeline.
    """

    @abstractmethod
    async def handle_async(self, event: Event) -> None:
        """
        Handle an event asynchronously.

        Args:
            event: The immutable event to process.
        """
        pass


class CallableSubscriber(Subscriber):
    """
    Wrapper to convert a callable into a Subscriber.
    """

    def __init__(self, handler: Callable[[Event], None]) -> None:
        self._handler = handler

    def handle(self, event: Event) -> None:
        self._handler(event)


def from_callable(handler: Callable[[Event], None]) -> Subscriber:
    """
    Create a subscriber from a callable.

    Args:
        handler: A callable that takes an Event and returns None.

    Returns:
        A Subscriber instance.
    """
    return CallableSubscriber(handler)
