# kernel/events/subscription.py
"""
Subscription metadata.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Subscription:
    """
    Immutable subscription metadata.

    Attributes:
        event_type: Event type to subscribe to (required).
        handler: Callable that handles the event (required).
        subscription_id: Unique identifier.
        priority: Execution priority.
        filter: Optional filter function.
        name: Optional human-readable name.
        enabled: Whether the subscription is active.
    """

    # Required fields first
    event_type: str
    handler: Callable

    # Optional fields with defaults
    subscription_id: UUID = field(default_factory=uuid4)
    priority: int = 0
    filter: Optional[Callable] = field(default=None, repr=False)
    name: Optional[str] = None
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.event_type:
            raise ValueError("Event type cannot be empty")
        if not callable(self.handler):
            raise ValueError("Handler must be callable")
