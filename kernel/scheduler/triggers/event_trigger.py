# kernel/scheduler/triggers/event_trigger.py
from datetime import datetime

from ..base.trigger import Trigger


class EventTrigger(Trigger):
    """Event-based trigger (stub for future extension)."""

    def __init__(self, event_type: str, filter: dict = None):
        self.event_type = event_type
        self.filter = filter or {}

    def next_run(self, from_time: datetime) -> datetime:
        return None

    def __repr__(self) -> str:
        return f"<EventTrigger event_type={self.event_type}>"
