# kernel/scheduler/registry/job_registry.py
from threading import RLock
from typing import Dict, List

from ..base.job import Job
from ..base.exceptions import JobNotFoundError


class JobRegistry:
    """Thread-safe registry for jobs."""

    def __init__(self):
        self._jobs: Dict[str, Job] = {}
        self._lock = RLock()

    def register(self, job: Job) -> None:
        with self._lock:
            self._jobs[job.name] = job

    def get(self, name: str) -> Job:
        with self._lock:
            if name not in self._jobs:
                raise JobNotFoundError(f"Job '{name}' not found")
            return self._jobs[name]

    def remove(self, name: str) -> None:
        with self._lock:
            if name in self._jobs:
                del self._jobs[name]

    def list(self) -> List[str]:
        with self._lock:
            return list(self._jobs.keys())

    def all(self) -> List[Job]:
        with self._lock:
            return list(self._jobs.values())

    def __len__(self) -> int:
        with self._lock:
            return len(self._jobs)

    def clear(self) -> None:
        with self._lock:
            self._jobs.clear()
