# kernel/scheduler/executor/job_executor.py
from .workflow_executor import WorkflowExecutor
from .retry_executor import RetryExecutor


class JobExecutor:
    def __init__(self, workflow_executor: WorkflowExecutor, retry_executor: RetryExecutor):
        self._workflow_executor = workflow_executor
        self._retry_executor = retry_executor

    def execute(self, job) -> dict:
        return self._retry_executor.execute(job)
