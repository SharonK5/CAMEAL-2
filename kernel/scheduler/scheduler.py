# kernel/scheduler/scheduler.py
import logging
import threading
import time
from datetime import datetime
from typing import Optional, List

from .registry.job_registry import JobRegistry
from .executor.job_executor import JobExecutor
from .base.job import Job
from .base.schedule import Schedule
from .base.trigger import Trigger
from .base.states import JobState
from .base.exceptions import SchedulerError
from .planner.scheduler_planner import SchedulerPlanner
from .events.scheduler_events import (
    JobScheduled, JobStarted, JobCompleted, JobFailed, JobRetrying, JobCancelled, JobPaused
)

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(
        self,
        registry: Optional[JobRegistry] = None,
        executor: Optional[JobExecutor] = None,
        event_bus=None,
        interval: int = 10,
    ):
        self._registry = registry or JobRegistry()
        self._executor = executor
        self._event_bus = event_bus
        self._interval = interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._schedules: dict = {}
        self._planner = SchedulerPlanner()

    def start(self) -> None:
        if self._running:
            return
        if not self._executor:
            raise SchedulerError("JobExecutor not provided")
        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("Scheduler started")

    def stop(self) -> None:
        if not self._running:
            return
        self._running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Scheduler stopped")

    def schedule(self, job: Job, trigger: Trigger) -> None:
        job.state = JobState.SCHEDULED
        next_run = self._planner.plan_next_run(job, trigger)
        job.next_run = next_run

        self._registry.register(job)
        self._schedules[job.name] = Schedule(job=job, trigger=trigger)

        if self._event_bus:
            self._event_bus.publish(JobScheduled(job.name, job.workflow, next_run))

        logger.info(f"Scheduled job: {job.name} (next run at {next_run})")

    def unschedule(self, name: str) -> None:
        if name in self._schedules:
            job = self._schedules[name].job
            job.state = JobState.CANCELLED
            if self._event_bus:
                self._event_bus.publish(JobCancelled(job.name, job.workflow, datetime.now()))
            del self._schedules[name]
        self._registry.remove(name)
        logger.info(f"Unscheduled job: {name}")

    def pause(self, name: str) -> None:
        schedule = self._schedules.get(name)
        if schedule:
            schedule.enabled = False
            schedule.job.state = JobState.PAUSED
            if self._event_bus:
                self._event_bus.publish(JobPaused(schedule.job.name, schedule.job.workflow, datetime.now()))
            logger.info(f"Paused job: {name}")

    def resume(self, name: str) -> None:
        schedule = self._schedules.get(name)
        if schedule:
            schedule.enabled = True
            schedule.job.state = JobState.SCHEDULED
            schedule.job.next_run = self._planner.plan_next_run(schedule.job, schedule.trigger)
            logger.info(f"Resumed job: {name}")

    def get_schedules(self) -> List[Schedule]:
        return list(self._schedules.values())

    def _loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                self._check_jobs()
            except Exception as e:
                logger.error(f"Scheduler loop error: {e}")
            time.sleep(self._interval)

    def _check_jobs(self) -> None:
        now = datetime.now()
        due = self._planner.get_due_jobs(list(self._schedules.values()), now)
        for schedule in due:
            self._execute_job(schedule.job)

    def _execute_job(self, job: Job) -> None:
        if not self._executor:
            return

        try:
            self._planner.update_job_state(job, JobState.RUNNING)
        except ValueError as e:
            logger.error(f"Cannot execute job '{job.name}': {e}")
            return

        if self._event_bus:
            self._event_bus.publish(JobStarted(job.name, job.workflow, datetime.now()))

        try:
            result = self._executor.execute(job)
            self._planner.update_job_state(job, JobState.COMPLETED)
            job.last_run = datetime.now()

            if job.name in self._schedules:
                trigger = self._schedules[job.name].trigger
                job.next_run = self._planner.plan_next_run(job, trigger)
                job.state = JobState.SCHEDULED

            if self._event_bus:
                self._event_bus.publish(JobCompleted(job.name, job.workflow, datetime.now(), result))

            logger.info(f"Job '{job.name}' completed successfully")

        except Exception as e:
            if job.retry_attempts < job.max_retries:
                job.retry_attempts += 1
                self._planner.update_job_state(job, JobState.RETRYING)
                if self._event_bus:
                    self._event_bus.publish(JobRetrying(
                        job.name, job.workflow, job.retry_attempts, job.max_retries,
                        datetime.now() + timedelta(seconds=job.retry_delay)
                    ))
                job.next_run = datetime.now() + timedelta(seconds=job.retry_delay)
                job.state = JobState.SCHEDULED
                logger.warning(f"Job '{job.name}' retry scheduled")
            else:
                self._planner.update_job_state(job, JobState.FAILED)
                job.last_run = datetime.now()
                if self._event_bus:
                    self._event_bus.publish(JobFailed(job.name, job.workflow, datetime.now(), str(e)))
                logger.error(f"Job '{job.name}' failed permanently: {e}")
