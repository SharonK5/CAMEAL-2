# Scheduler API Reference

## Public API

### `Job`

```python
@dataclass
class Job:
    name: str
    workflow: str
    enabled: bool = True
    retry_attempts: int = 0
    retry_delay: int = 60
    max_retries: int = 3
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    state: JobState = JobState.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)
Trigger (ABC)
python
Copy
Download
class Trigger(ABC):
    @abstractmethod
    def next_run(self, from_time: datetime) -> datetime:
        pass
CronTrigger
python
Copy
Download
class CronTrigger(Trigger):
    def __init__(self, expression: str):
        ...
IntervalTrigger
python
Copy
Download
class IntervalTrigger(Trigger):
    def __init__(self, seconds: int):
        ...
OnceTrigger
python
Copy
Download
class OnceTrigger(Trigger):
    def __init__(self, run_at: datetime):
        ...
EventTrigger (future extension)
python
Copy
Download
class EventTrigger(Trigger):
    def __init__(self, event_type: str, filter: dict = None):
        ...
JobState
python
Copy
Download
class JobState(Enum):
    PENDING = auto()
    SCHEDULED = auto()
    READY = auto()
    RUNNING = auto()
    RETRYING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()
    PAUSED = auto()
JobRegistry
python
Copy
Download
class JobRegistry:
    def register(self, job: Job) -> None
    def get(self, name: str) -> Job
    def remove(self, name: str) -> None
    def list(self) -> List[str]
    def all(self) -> List[Job]
    def __len__(self) -> int
    def clear(self) -> None
SchedulerPlanner
python
Copy
Download
class SchedulerPlanner:
    @classmethod
    def get_due_jobs(cls, schedules: List[Schedule], now: Optional[datetime] = None) -> List[Schedule]
    @classmethod
    def plan_next_run(cls, job: Job, trigger) -> Optional[datetime]
    @classmethod
    def update_job_state(cls, job: Job, state: JobState) -> None
WorkflowExecutor
python
Copy
Download
class WorkflowExecutor:
    def __init__(self, orchestrator: Orchestrator)
    def execute(self, job: Job) -> dict
RetryExecutor
python
Copy
Download
class RetryExecutor:
    def __init__(
        self,
        workflow_executor: WorkflowExecutor,
        default_max_retries: int = 3,
        default_delay: int = 60,
        backoff_factor: float = 2.0,
        jitter: bool = True,
    )
    def execute(self, job: Job) -> dict
Scheduler
python
Copy
Download
class Scheduler:
    def __init__(
        self,
        registry: Optional[JobRegistry] = None,
        executor: Optional[JobExecutor] = None,
        event_bus=None,
        interval: int = 10,
    )
    def start(self) -> None
    def stop(self) -> None
    def schedule(self, job: Job, trigger: Trigger) -> None
    def unschedule(self, name: str) -> None
    def pause(self, name: str) -> None
    def resume(self, name: str) -> None
    def get_schedules(self) -> List[Schedule]
Events
The scheduler publishes the following events to the EventBus:

Event	Description
JobScheduled	A job has been scheduled with a trigger.
JobStarted	A job has started executing.
JobCompleted	A job completed successfully.
JobFailed	A job failed permanently.
JobRetrying	A job is being retried.
JobCancelled	A job was cancelled.
JobPaused	A job was paused.
JobResumed	A paused job was resumed.
Example
python
Copy
Download
from kernel.scheduler import Scheduler, Job, CronTrigger
from kernel.orchestrator import Orchestrator

orchestrator = Orchestrator(...)
scheduler = Scheduler(orchestrator=orchestrator)

job = Job(
    name="daily_ingestion",
    workflow="ingest_documents",
    max_retries=3,
)

scheduler.schedule(job, CronTrigger("0 0 * * *"))
scheduler.start()
text
Copy
Download

---

## 📄 `kernel/scheduler/manifest.yaml`

```yaml
# kernel/scheduler/manifest.yaml
name: scheduler
version: 1.0.0
description: Automated workflow scheduling subsystem
author: CAMEAL Kernel Team
kernel_compatibility: ">=1.0.0"

providers: []
engines: []
workflows: []
schedulers: []

dependencies:
  - kernel.lifecycle
  - kernel.events
  - kernel.orchestrator
  - kernel.workflows
  - kernel.managers

# Public API exports
exports:
  - Job
  - JobState
  - Trigger
  - CronTrigger
  - IntervalTrigger
  - OnceTrigger
  - EventTrigger
  - JobRegistry
  - SchedulerPlanner
  - WorkflowExecutor
  - RetryExecutor
  - Scheduler
  - SchedulerLifecycle

events:
  emitted:
    - JobScheduled
    - JobStarted
    - JobCompleted
    - JobFailed
    - JobRetrying
    - JobCancelled
    - JobPaused
    - JobResumed
