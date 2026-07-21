# kernel/scheduler/base/schedule.py
from dataclasses import dataclass

from .job import Job
from .trigger import Trigger


@dataclass
class Schedule:
    """Binds a job with a trigger."""

    job: Job
    trigger: Trigger
    enabled: bool = True

    def __repr__(self) -> str:
        return f"<Schedule job={self.job.name}, trigger={self.trigger}>"
