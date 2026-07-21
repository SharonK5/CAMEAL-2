# kernel/scheduler/executor/retry_executor.py
import logging
import time
import random

from ..base.job import Job
from ..base.exceptions import JobExecutionError
from .workflow_executor import WorkflowExecutor

logger = logging.getLogger(__name__)


class RetryExecutor:
    def __init__(
        self,
        workflow_executor: WorkflowExecutor,
        default_max_retries: int = 3,
        default_delay: int = 60,
        backoff_factor: float = 2.0,
        jitter: bool = True,
    ):
        self._workflow_executor = workflow_executor
        self._default_max_retries = default_max_retries
        self._default_delay = default_delay
        self._backoff_factor = backoff_factor
        self._jitter = jitter

    def execute(self, job: Job) -> dict:
        max_retries = job.max_retries or self._default_max_retries
        delay = job.retry_delay or self._default_delay

        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    logger.info(f"Retry attempt {attempt} for job '{job.name}'")
                return self._workflow_executor.execute(job)
            except JobExecutionError as e:
                if attempt >= max_retries:
                    raise JobExecutionError(f"Job '{job.name}' failed after {max_retries + 1} attempts") from e
                wait = delay * (self._backoff_factor ** attempt)
                if self._jitter:
                    wait += random.uniform(0, wait * 0.1)
                logger.warning(f"Job '{job.name}' failed (attempt {attempt+1}), retrying in {wait:.1f}s")
                time.sleep(wait)
