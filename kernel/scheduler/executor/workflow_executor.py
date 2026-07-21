# kernel/scheduler/executor/workflow_executor.py
import logging
from datetime import datetime

from ...orchestrator import Orchestrator
from ...models import Request
from ..base.job import Job
from ..base.exceptions import JobExecutionError

logger = logging.getLogger(__name__)


class WorkflowExecutor:
    def __init__(self, orchestrator: Orchestrator):
        self._orchestrator = orchestrator

    def execute(self, job: Job) -> dict:
        logger.info(f"Executing job: {job.name} (workflow: {job.workflow})")
        request = Request(
            request_id=f"scheduler-{job.name}-{datetime.now().isoformat()}",
            workflow_name=job.workflow,
            metadata={"job_name": job.name},
        )
        try:
            response = self._orchestrator.execute(request)
            job.last_run = datetime.now()
            return response
        except Exception as e:
            raise JobExecutionError(f"Workflow '{job.workflow}' failed: {e}") from e
