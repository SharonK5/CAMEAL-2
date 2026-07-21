# kernel/scheduler/planner/scheduler_planner.py
from datetime import datetime
from typing import List, Optional

from ..base.job import Job
from ..base.states import JobState
from ..base.schedule import Schedule


class SchedulerPlanner:
    """Time-based execution planner for the scheduler."""

    @classmethod
    def get_due_jobs(cls, schedules: List[Schedule], now: Optional[datetime] = None) -> List[Schedule]:
        if now is None:
            now = datetime.now()
        return [s for s in schedules if s.enabled and s.job.enabled and s.job.next_run and s.job.next_run <= now]

    @classmethod
    def plan_next_run(cls, job: Job, trigger) -> Optional[datetime]:
        if not job.enabled:
            return None
        if job.last_run:
            return trigger.next_run(job.last_run)
        return trigger.next_run(datetime.now())

    @classmethod
    def update_job_state(cls, job: Job, state: JobState) -> None:
        valid_transitions = {
            JobState.PENDING: {JobState.SCHEDULED, JobState.CANCELLED},
            JobState.SCHEDULED: {JobState.READY, JobState.PAUSED, JobState.CANCELLED},
            JobState.READY: {JobState.RUNNING, JobState.PAUSED, JobState.CANCELLED},
            JobState.RUNNING: {JobState.COMPLETED, JobState.FAILED, JobState.RETRYING},
            JobState.RETRYING: {JobState.RUNNING, JobState.FAILED, JobState.CANCELLED},
            JobState.COMPLETED: set(),
            JobState.FAILED: set(),
            JobState.CANCELLED: set(),
            JobState.PAUSED: {JobState.SCHEDULED, JobState.READY, JobState.CANCELLED},
        }
        if state not in valid_transitions.get(job.state, set()):
            raise ValueError(f"Invalid transition from {job.state} to {state} for job '{job.name}'")
        job.state = state
