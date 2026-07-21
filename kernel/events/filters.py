# kernel/events/filters.py
"""
Event filters.

Filters are used by subscribers to selectively process events based on
event properties. Filters are pure functions that return True if the
event should be processed.

Filters can be composed using combine() and any().
"""

from typing import Callable, Any, Dict, Optional

from .event import Event


class EventFilter:
    """
    Collection of event filter factories.

    Filters are callables: filter(event: Event) -> bool
    """

    @staticmethod
    def by_type(event_type: str) -> Callable[[Event], bool]:
        """Filter events by type (exact match)."""
        return lambda e: e.event_type == event_type

    @staticmethod
    def by_type_prefix(prefix: str) -> Callable[[Event], bool]:
        """Filter events by type prefix."""
        return lambda e: e.event_type.startswith(prefix)

    @staticmethod
    def by_source(source: str) -> Callable[[Event], bool]:
        """Filter events by source component."""
        return lambda e: e.source == source

    @staticmethod
    def by_category(category: str) -> Callable[[Event], bool]:
        """Filter events by category."""
        return lambda e: e.category == category

    @staticmethod
    def by_payload_field(field: str, value: Any) -> Callable[[Event], bool]:
        """Filter events by a payload field value."""
        return lambda e: e.payload.get(field) == value

    @staticmethod
    def by_payload_field_exists(field: str) -> Callable[[Event], bool]:
        """Filter events that have a specific payload field."""
        return lambda e: field in e.payload

    @staticmethod
    def by_trace_id(trace_id: str) -> Callable[[Event], bool]:
        """Filter events by trace ID."""
        return lambda e: e.trace_id == trace_id

    @staticmethod
    def by_correlation_id(correlation_id: str) -> Callable[[Event], bool]:
        """Filter events by correlation ID."""
        return lambda e: e.correlation_id == correlation_id

    @staticmethod
    def by_priority(priority: str) -> Callable[[Event], bool]:
        """Filter events by priority."""
        return lambda e: e.priority == priority

    @staticmethod
    def combine(*filters: Callable[[Event], bool]) -> Callable[[Event], bool]:
        """Combine multiple filters with AND logic."""
        return lambda e: all(f(e) for f in filters)

    @staticmethod
    def any(*filters: Callable[[Event], bool]) -> Callable[[Event], bool]:
        """Combine multiple filters with OR logic."""
        return lambda e: any(f(e) for f in filters)

    @staticmethod
    def not_(filter_func: Callable[[Event], bool]) -> Callable[[Event], bool]:
        """Negate a filter."""
        return lambda e: not filter_func(e)
