# kernel/scheduler/base/job.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

from .states import JobState


@dataclass
class Job:
    """A job that runs a workflow on a schedule."""

    name: str
    workflow: str
    enabled: bool = True
    retry_attempts: int = 0
    retry_delay: int = 60
    max_retries: int = 3
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    state: JobState = JobState.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"<Job name={self.name}, workflow={self.workflow}, state={self.state}>"
