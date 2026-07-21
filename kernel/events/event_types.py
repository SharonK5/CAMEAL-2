# kernel/events/event_types.py
"""
Standard kernel event types.

Re-exports the EventType catalog and category definitions for convenience.
"""

from .event import EventType, EventCategory, EventPriority
from .event import Event

__all__ = [
    "EventType",
    "EventCategory",
    "EventPriority",
    "Event",
]
