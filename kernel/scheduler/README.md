# CAMEAL Kernel Scheduler

## Overview

The CAMEAL Kernel Scheduler is the subsystem responsible for automated, time‑based execution of workflows. It integrates with the existing `WorkflowRegistry` and `Orchestrator` to run workflows on a schedule, at intervals, or in response to events.

The scheduler is **not** a general‑purpose task runner. It is specifically designed to schedule workflows—declarative execution graphs—which are then executed by the orchestrator. This preserves the separation of concerns established throughout the kernel.

## Why It Exists

As the kernel matures, many workflows need to run automatically:

- Periodic data ingestion (e.g., every hour)
- Daily report generation (e.g., at midnight)
- Model retraining (e.g., weekly)
- Health checks (e.g., every minute)
- One‑off cleanup jobs (e.g., after a deployment)

Without a scheduler, these tasks would have to be triggered manually or via external cron jobs, bypassing the kernel's lifecycle, event system, and observability.

The scheduler brings these automated executions into the kernel's managed runtime, providing:

- **Centralised management** – all scheduled jobs are registered and visible.
- **Lifecycle integration** – jobs start and stop with the kernel.
- **Observability** – job events are emitted and can be monitored.
- **Consistency** – execution follows the same path as manual workflow runs.

## Responsibilities

The scheduler is responsible for:

- **Job definition** – capturing what workflow to run, when, and with what retry policy.
- **Trigger evaluation** – determining when a job should next run (cron, interval, one‑shot, event).
- **Execution coordination** – handing the workflow to the orchestrator at the right time.
- **State management** – tracking job state transitions (scheduled, running, completed, failed, etc.).
- **Retry handling** – retrying failed jobs with configurable backoff and limits.
- **Event emission** – publishing lifecycle events for monitoring and diagnostics.

The scheduler does **not**:

- Execute domain logic (ML, RAG, governance, etc.)
- Interact directly with providers or plugins
- Contain business rules or policies

## Architecture

The scheduler is composed of the following major components:
┌─────────────────────────────────────────────────────────┐
│ Scheduler │
│ │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Planner │ │
│ │ (determines which jobs are due and their │ │
│ │ next execution time) │ │
│ └────────────────────┬────────────────────────────┘ │
│ │ │
│ ┌────────────────────▼────────────────────────────┐ │
│ │ Job Registry │ │
│ │ (thread‑safe storage of all jobs) │ │
│ └────────────────────┬────────────────────────────┘ │
│ │ │
│ ┌────────────────────▼────────────────────────────┐ │
│ │ Job Executor │ │
│ │ ┌────────────────────────────────────────┐ │ │
│ │ │ Workflow Executor │ │ │
│ │ └────────────────────────────────────────┘ │ │
│ │ ┌────────────────────────────────────────┐ │ │
│ │ │ Retry Executor │ │ │
│ │ └────────────────────────────────────────┘ │ │
│ └────────────────────┬────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌──────────────────┐ │
│ │ Orchestrator │ │
│ └──────────────────┘ │
└─────────────────────────────────────────────────────────┘

text
Copy
Download

## Execution Flow

1. A job is created with a name, workflow name, and trigger (cron, interval, or one‑shot).
2. The scheduler registers the job and calculates its first `next_run` time.
3. In the main loop, the planner checks all scheduled jobs.
4. For each due job, the executor passes it to the orchestrator via the `WorkflowExecutor`.
5. The orchestrator executes the workflow (invoking plugins, providers, etc.).
6. On success, the job is marked `COMPLETED` and its next run is recalculated.
7. On failure, the retry executor handles retries with exponential backoff.
8. Job lifecycle events are emitted at each stage.

## Integration with Other Subsystems

| Subsystem      | Role                                                          |
|----------------|---------------------------------------------------------------|
| **Workflows**  | The scheduler runs workflows.                                 |
| **Orchestrator** | Executes the workflow on behalf of the scheduler.           |
| **Events**     | The scheduler emits job lifecycle events.                     |
| **Lifecycle**  | The scheduler participates in the kernel's start/stop cycle.  |
| **Managers**   | Integrates with `SchedulerManager` for registry.              |

## Examples

### Schedule a daily workflow

```python
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
Schedule a one‑shot job
python
Copy
Download
from datetime import datetime, timedelta
from kernel.scheduler import OnceTrigger

job = Job(name="cleanup", workflow="cleanup_cache")
scheduler.schedule(job, OnceTrigger(datetime.now() + timedelta(hours=1)))
References
ARCHITECTURE.md – Detailed architecture and design principles.

DESIGN.md – Design decisions and trade‑offs.

API.md – Public API reference.

EXECUTION_FLOW.md – End‑to‑end execution walkthrough.

EXTENSION_GUIDE.md – How to extend the scheduler.
