import pytest
from unittest.mock import Mock
from kernel.scheduler import Scheduler, Job, IntervalTrigger, SchedulerLifecycle, JobState


def test_scheduler_lifecycle():
    executor = Mock()
    scheduler = Scheduler(executor=executor)
    lifecycle = SchedulerLifecycle(scheduler)
    assert lifecycle.health().value == "unhealthy"
    lifecycle.start()
    assert lifecycle.health().value == "healthy"
    lifecycle.stop()
    assert lifecycle.health().value == "unhealthy"


def test_schedule_job():
    executor = Mock()
    scheduler = Scheduler(executor=executor)
    job = Job(name="test", workflow="wf")
    trigger = IntervalTrigger(60)
    scheduler.schedule(job, trigger)
    assert job.state == JobState.SCHEDULED
    assert job.next_run is not None
    schedules = scheduler.get_schedules()
    assert len(schedules) == 1
    assert schedules[0].job.name == "test"
