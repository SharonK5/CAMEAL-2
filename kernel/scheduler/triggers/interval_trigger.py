# kernel/scheduler/triggers/interval_trigger.py
from datetime import datetime, timedelta

from ..base.trigger import Trigger
from ..base.exceptions import InvalidTriggerError


class IntervalTrigger(Trigger):
    def __init__(self, seconds: int):
        if seconds <= 0:
            raise InvalidTriggerError("Interval must be positive")
        self.seconds = seconds

    def next_run(self, from_time: datetime) -> datetime:
        return from_time + timedelta(seconds=self.seconds)

    def __repr__(self) -> str:
        return f"<IntervalTrigger seconds={self.seconds}>"
