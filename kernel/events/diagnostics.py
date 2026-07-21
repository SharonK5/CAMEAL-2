# kernel/events/diagnostics.py
"""
Event diagnostics and observability.
"""

import time
from typing import Dict, List, Any, Optional
from threading import RLock

from .event import Event


class Diagnostics:
    """
    Records event metrics and traces.
    """

    def __init__(self) -> None:
        self._publish_count: Dict[str, int] = {}
        self._error_count: Dict[str, int] = {}
        self._processing_time: Dict[str, List[float]] = {}
        self._lock = RLock()

    def record_publish(self, event: Event) -> None:
        """Record an event publication."""
        with self._lock:
            self._publish_count[event.event_type] = self._publish_count.get(event.event_type, 0) + 1

    def record_error(self, event: Event, error: Exception) -> None:
        """Record an event error."""
        with self._lock:
            self._error_count[event.event_type] = self._error_count.get(event.event_type, 0) + 1

    def record_processing_time(self, event_type: str, duration_ms: float) -> None:
        """Record event processing time."""
        with self._lock:
            self._processing_time.setdefault(event_type, []).append(duration_ms)

    def get_metrics(self) -> Dict[str, Any]:
        """Get event metrics."""
        with self._lock:
            return {
                "publish_counts": dict(self._publish_count),
                "error_counts": dict(self._error_count),
                "total_events": sum(self._publish_count.values()),
                "total_errors": sum(self._error_count.values()),
                "avg_processing_time": {
                    k: sum(v) / len(v) if v else 0
                    for k, v in self._processing_time.items()
                },
            }
