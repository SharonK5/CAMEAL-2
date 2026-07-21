# Scheduler Architecture

## Design Principles

The scheduler is built on the same architectural principles as the rest of the CAMEAL Kernel:

1. **Single Responsibility** – Each component has a narrow, well‑defined purpose.
2. **Separation of Concerns** – Planning, execution, and state management are distinct.
3. **Explicit State** – Job states are first‑class concepts with controlled transitions.
4. **Event‑Driven** – The scheduler emits events for every significant occurrence.
5. **Thread‑Safety** – The scheduler is designed for concurrent access.
6. **Lifecycle Awareness** – The scheduler participates in the kernel’s start/stop cycle.

## Core Concepts

### Job

A `Job` is the unit of work. It contains:

- `name` – unique identifier
- `workflow` – name of the workflow to execute
- `enabled` – whether the job is active
- `state` – current state (PENDING, SCHEDULED, RUNNING, etc.)
- `next_run` – next scheduled execution time
- `max_retries` / `retry_attempts` – retry policy
- `metadata` – additional data

### Trigger

A `Trigger` defines when a job should run. The scheduler supports:

- **CronTrigger** – cron expressions (e.g., `"0 0 * * *"`)
- **IntervalTrigger** – fixed intervals (e.g., every 60 seconds)
- **OnceTrigger** – a specific point in time
- **EventTrigger** – (future) event‑based triggering

### Schedule

A `Schedule` binds a `Job` with a `Trigger`. It is the primary object managed by the scheduler.

### Job State Machine

The scheduler uses an explicit state machine to track job lifecycle:
PENDING
│
▼
SCHEDULED
│
├───────► READY
│ │
│ ▼
│ RUNNING
│ │
│ ┌─────┴─────┐
│ ▼ ▼
│ COMPLETED RETRYING
│ │
│ ▼
│ RUNNING (retry)
│ │
│ ┌───┴───┐
│ ▼ ▼
│ COMPLETED FAILED
│
├───────► PAUSED
│ │
│ ▼
│ SCHEDULED (resume)
│
└───────► CANCELLED

text
Copy
Download

Valid transitions are defined in `base/states.py`. Any invalid transition raises an exception.

## Component Details

### 1. Planner

The planner is responsible for time‑based decision making:

- **`get_due_jobs()`** – returns all schedules whose `next_run` ≤ current time.
- **`plan_next_run()`** – calculates the next execution time using the trigger.
- **`update_job_state()`** – validates and applies state transitions.

This separation ensures that scheduling logic is decoupled from execution.

### 2. Job Registry

A thread‑safe registry (`job_registry.py`) that stores all jobs by name. It provides:

- `register()`, `get()`, `remove()`, `list()`, `all()`
- `__len__` and iteration

### 3. Executors

The scheduler uses a chain of executors:

- **JobExecutor** – orchestrates the overall execution flow (handles retries, state updates).
- **WorkflowExecutor** – communicates with the orchestrator to run the workflow.
- **RetryExecutor** – implements exponential backoff and retry limits.

### 4. Scheduler Loop

The scheduler runs a background thread that periodically:

1. Checks for due jobs using the planner.
2. For each due job, invokes the job executor.
3. Updates job state and next_run based on the outcome.
4. Sleeps for a configurable interval.

## Event Model

All significant events are published to the kernel’s `EventBus`:

| Event               | Description                                       |
|---------------------|---------------------------------------------------|
| `JobScheduled`      | A job has been scheduled with a trigger.          |
| `JobStarted`        | A job has started executing.                      |
| `JobCompleted`      | A job completed successfully.                     |
| `JobFailed`         | A job failed permanently.                         |
| `JobRetrying`       | A job is being retried.                           |
| `JobCancelled`      | A job was cancelled by the user.                  |
| `JobPaused`         | A job was paused.                                 |
| `JobResumed`        | A paused job was resumed.                         |

These events enable monitoring, alerting, and integration with diagnostics.

## Lifecycle Integration

The scheduler is a `Lifecycle` component:

- **`start()`** – begins the background loop.
- **`stop()`** – stops the loop and waits for ongoing executions to complete (graceful shutdown).
- **`health()`** – reports `HEALTHY` if the scheduler loop is running.

The scheduler is managed by `SchedulerManager` (in `kernel/managers`) and started/stopped as part of the kernel’s bootstrap process.

## Thread Safety

- The job registry uses a reentrant lock (`RLock`) for all operations.
- The scheduler loop is single‑threaded (no concurrent execution of the same job).
- The executor may be invoked concurrently by the loop (if multiple jobs are due), but each job execution is isolated.

## Extensibility

The scheduler is designed to be extended:

- New trigger types can be added by subclassing `Trigger`.
- Alternative planners can be implemented for different scheduling strategies (e.g., priority‑based).
- Custom retry policies can be added via the retry executor.
- Plugins can register new jobs during activation.

## Security Considerations

- Job metadata should not contain secrets; use the `SecretsProvider` for sensitive data.
- Job names and workflow names should be validated against injection attacks.
- The scheduler should not execute untrusted workflows; workflows must be registered and validated.

## Testing Strategy

- **Unit tests** – each component is tested in isolation.
- **Integration tests** – the scheduler is tested with a mock orchestrator.
- **State transition tests** – all possible state transitions are validated.
- **Concurrency tests** – the registry and loop are tested for thread safety.

## Dependencies

The scheduler depends on:

- `kernel.lifecycle` – for lifecycle management.
- `kernel.events` – for event publishing.
- `kernel.orchestrator` – for workflow execution.
- `kernel.workflows` – for workflow definitions.
- `kernel.managers` – for `SchedulerManager`.

It does **not** depend on providers, plugins, or domain logic.
