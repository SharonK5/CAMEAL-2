# kernel/events/priority.py
"""
Event priority definitions.

Defines the priority levels used for event ordering.
"""

from enum import Enum


class EventPriority(str, Enum):
    """
    Priority levels for event ordering.

    Higher priority events are dispatched before lower priority events.
    """

    CRITICAL = "critical"   # Security, shutdown, system-critical events
    HIGH = "high"           # Workflow execution, request processing
    NORMAL = "normal"       # Standard events (default)
    LOW = "low"             # Notifications, non-critical updates
    BACKGROUND = "background"  # Learning, indexing, monitoring

    def __lt__(self, other: "EventPriority") -> bool:
        order = [
            EventPriority.CRITICAL,
            EventPriority.HIGH,
            EventPriority.NORMAL,
            EventPriority.LOW,
            EventPriority.BACKGROUND,
        ]
        return order.index(self) < order.index(other)

    def __le__(self, other: "EventPriority") -> bool:
        return self.__lt__(other) or self == other

    def __gt__(self, other: "EventPriority") -> bool:
        return not self.__le__(other)

    def __ge__(self, other: "EventPriority") -> bool:
        return not self.__lt__(other)
