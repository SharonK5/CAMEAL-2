# kernel/scheduler/triggers/cron_trigger.py
from datetime import datetime
from croniter import croniter

from ..base.trigger import Trigger
from ..base.exceptions import InvalidTriggerError


class CronTrigger(Trigger):
    def __init__(self, expression: str):
        self.expression = expression
        try:
            croniter(expression)
        except Exception as e:
            raise InvalidTriggerError(f"Invalid cron expression: {e}")

    def next_run(self, from_time: datetime) -> datetime:
        return croniter(self.expression, from_time).get_next(datetime)

    def __repr__(self) -> str:
        return f"<CronTrigger expression={self.expression}>"
