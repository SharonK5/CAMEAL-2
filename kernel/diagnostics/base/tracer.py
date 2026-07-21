import logging
from collections import deque
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class Tracer:
    def __init__(self, trace_limit: int = 100):
        self._trace_limit = trace_limit
        self._traces: deque = deque(maxlen=trace_limit)

    def record(self, event) -> None:
        try:
            event_dict = self._normalize_event(event)
            if event_dict and self._is_trace_event(event_dict):
                self._traces.append(event_dict)
        except Exception as e:
            logger.error(f"Error processing trace event: {e}")

    def get_traces(self, limit: Optional[int] = None) -> List[Dict]:
        limit = limit or self._trace_limit
        return list(self._traces)[-limit:]

    def clear(self) -> None:
        self._traces.clear()

    def _normalize_event(self, event) -> Dict:
        if isinstance(event, dict):
            return event
        if hasattr(event, "event_type"):
            result = {"type": event.event_type}
            if hasattr(event, "payload") and isinstance(event.payload, dict):
                result.update(event.payload)
            if hasattr(event, "metadata") and isinstance(event.metadata, dict):
                result.update(event.metadata)
            return result
        if hasattr(event, "to_dict"):
            return event.to_dict()
        return {"type": type(event).__name__, "payload": str(event)}

    def _is_trace_event(self, event_dict: Dict) -> bool:
        trace_types = (
            "workflow.started", "workflow.completed", "workflow.failed",
            "job.started", "job.completed", "job.failed",
            "orchestrator.execute", "plugin.invoke", "provider.call",
            "component.started", "component.stopped",
        )
        return event_dict.get("type") in trace_types
