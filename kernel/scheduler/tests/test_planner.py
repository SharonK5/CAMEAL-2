import pytest
from datetime import datetime, timedelta
from kernel.scheduler.planner import SchedulerPlanner
from kernel.scheduler.base import Job, Schedule, JobState
from kernel.scheduler.triggers import IntervalTrigger


def test_get_due_jobs():
    job = Job(name="test", workflow="wf")
    trigger = IntervalTrigger(60)
    job.next_run = datetime.now() - timedelta(seconds=10)
    schedule = Schedule(job=job, trigger=trigger)

    due = SchedulerPlanner.get_due_jobs([schedule])
    assert len(due) == 1
    assert due[0].job.name == "test"


def test_plan_next_run():
    job = Job(name="test", workflow="wf")
    trigger = IntervalTrigger(60)
    next_run = SchedulerPlanner.plan_next_run(job, trigger)
    assert next_run > datetime.now()


def test_state_transition():
    job = Job(name="test", workflow="wf", state=JobState.SCHEDULED)
    SchedulerPlanner.update_job_state(job, JobState.READY)
    assert job.state == JobState.READY
    with pytest.raises(ValueError):
        SchedulerPlanner.update_job_state(job, JobState.COMPLETED)  # invalid
