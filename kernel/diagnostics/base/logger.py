# kernel/diagnostics/base/logger.py
import logging
from collections import deque
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class Logger:
    def __init__(self, log_limit: int = 500):
        self._log_limit = log_limit
        self._logs: deque = deque(maxlen=log_limit)

    def record(self, event) -> None:
        try:
            event_dict = self._normalize_event(event)
            if event_dict and self._is_log_event(event_dict):
                if "timestamp" not in event_dict:
                    import time
                    event_dict["timestamp"] = time.time()
                self._logs.append(event_dict)
        except Exception as e:
            logger.error(f"Error processing log event: {e}")

    def get_logs(self, limit: Optional[int] = None, level: Optional[str] = None) -> List[Dict]:
        result = list(self._logs)
        if level:
            result = [l for l in result if l.get("level") == level]
        if limit:
            result = result[-limit:]
        return result

    def clear(self) -> None:
        self._logs.clear()

    def _normalize_event(self, event) -> Dict:
        if isinstance(event, dict):
            return event
        if hasattr(event, "event_type"):
            event_type = event.event_type
            level = None
            if event_type.startswith("log."):
                level = event_type.split(".", 1)[1]
            # Start with the event type and level
            result = {
                "type": event_type,
                "level": level,
            }
            # Add payload fields directly (if any)
            if hasattr(event, "payload") and isinstance(event.payload, dict):
                result.update(event.payload)
            # Add metadata fields
            if hasattr(event, "metadata") and isinstance(event.metadata, dict):
                result.update(event.metadata)
            return result
        if hasattr(event, "to_dict"):
            return event.to_dict()
        return {"type": type(event).__name__, "payload": str(event)}

    def _is_log_event(self, event_dict: Dict) -> bool:
        log_types = (
            "log.debug", "log.info", "log.warn", "log.warning", "log.error", "log.fatal",
            "system.info", "system.warning", "system.error",
            "component.status", "component.event",
        )
        return event_dict.get("type") in log_types
