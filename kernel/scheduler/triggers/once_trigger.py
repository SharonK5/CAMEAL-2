# kernel/scheduler/triggers/once_trigger.py
from datetime import datetime

from ..base.trigger import Trigger


class OnceTrigger(Trigger):
    def __init__(self, run_at: datetime):
        self.run_at = run_at

    def next_run(self, from_time: datetime) -> datetime:
        if from_time >= self.run_at:
            return None
        return self.run_at

    def __repr__(self) -> str:
        return f"<OnceTrigger run_at={self.run_at}>"
