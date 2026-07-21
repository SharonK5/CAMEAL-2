# kernel/scheduler/events/scheduler_events.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class JobScheduled:
    job_name: str
    workflow: str
    next_run: datetime


@dataclass
class JobStarted:
    job_name: str
    workflow: str
    timestamp: datetime


@dataclass
class JobCompleted:
    job_name: str
    workflow: str
    timestamp: datetime
    result: Optional[dict] = None


@dataclass
class JobFailed:
    job_name: str
    workflow: str
    timestamp: datetime
    error: str


@dataclass
class JobRetrying:
    job_name: str
    workflow: str
    attempt: int
    max_retries: int
    next_retry: datetime


@dataclass
class JobCancelled:
    job_name: str
    workflow: str
    timestamp: datetime


@dataclass
class JobPaused:
    job_name: str
    workflow: str
    timestamp: datetime


@dataclass
class JobResumed:
    job_name: str
    workflow: str
    timestamp: datetime
