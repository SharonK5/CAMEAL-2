# kernel/events/exceptions.py
"""
Event-specific exceptions.
"""


class EventError(Exception):
    """Base exception for all event-related errors."""


class EventValidationError(EventError):
    """Raised when event validation fails."""


class EventDispatchError(EventError):
    """Raised when event dispatch fails."""


class EventSubscriptionError(EventError):
    """Raised when subscription operations fail."""


class EventSerializationError(EventError):
    """Raised when event serialization fails."""


class EventBusError(EventError):
    """Raised when an event bus operation fails."""
