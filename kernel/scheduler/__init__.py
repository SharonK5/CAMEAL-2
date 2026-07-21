# kernel/scheduler/__init__.py
"""
CAMEAL Kernel Scheduler.

Automated execution of workflows on a schedule.
"""

from .base.job import Job
from .base.states import JobState
from .base.trigger import Trigger
from .base.schedule import Schedule
from .base.exceptions import (
    SchedulerError,
    JobNotFoundError,
    JobExecutionError,
    InvalidTriggerError,
    ScheduleError,
)

from .registry.job_registry import JobRegistry

from .planner.scheduler_planner import SchedulerPlanner

from .executor.job_executor import JobExecutor
from .executor.workflow_executor import WorkflowExecutor
from .executor.retry_executor import RetryExecutor

from .triggers.cron_trigger import CronTrigger
from .triggers.interval_trigger import IntervalTrigger
from .triggers.once_trigger import OnceTrigger
from .triggers.event_trigger import EventTrigger

from .scheduler import Scheduler
from .lifecycle import SchedulerLifecycle

__all__ = [
    # Core
    "Job",
    "JobState",
    "Trigger",
    "Schedule",
    "Scheduler",
    "SchedulerLifecycle",

    # Registry
    "JobRegistry",

    # Planner
    "SchedulerPlanner",

    # Executors
    "JobExecutor",
    "WorkflowExecutor",
    "RetryExecutor",

    # Triggers
    "CronTrigger",
    "IntervalTrigger",
    "OnceTrigger",
    "EventTrigger",

    # Exceptions
    "SchedulerError",
    "JobNotFoundError",
    "JobExecutionError",
    "InvalidTriggerError",
    "ScheduleError",
]
