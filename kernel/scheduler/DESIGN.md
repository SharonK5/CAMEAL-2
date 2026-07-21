# Scheduler Design

## Design Philosophy

The scheduler is built on the same design principles as the rest of the CAMEAL Kernel:

- **Explicit over implicit** – State machines, triggers, and schedules are first‑class concepts.
- **Separation of concerns** – Planning, execution, and state management are decoupled.
- **Testability** – Each component is isolated and testable.
- **Extensibility** – New trigger types and scheduling strategies can be added without modifying core logic.

## Key Design Decisions

### 1. Schedule as a First‑Class Concept

A `Schedule` explicitly binds a `Job` with a `Trigger`. This makes the relationship clear and allows the same job to be scheduled with different triggers without duplication.

### 2. Explicit Job State Machine

Job states are defined as an enum (`JobState`) with controlled transitions. This prevents invalid state changes and makes the scheduler’s behaviour predictable.

### 3. Planner Separation

The planner is responsible for determining due jobs and calculating next run times. This keeps the scheduler loop simple and focused on orchestration.

### 4. Retry as an Executor Wrapper

Retry logic is implemented in a separate executor (`RetryExecutor`) that wraps the `WorkflowExecutor`. This makes retry policies configurable and testable independently.

### 5. Event‑Driven Observability

The scheduler emits lifecycle events via the kernel’s `EventBus`. This allows monitoring, logging, and diagnostics without coupling them to the scheduler logic.

## Trade‑Offs

### Single‑Threaded Loop vs. Parallel Execution

The scheduler runs on a single background thread. This simplifies the design and ensures that jobs are executed in a predictable order. If parallel execution is needed, it can be added as an extension later.

### In‑Memory vs. Persistent State

The job registry is in‑memory. This is sufficient for most use cases and keeps the design simple. For production scenarios that require persistence, the registry can be extended to use a backing store.

### Cron Validation at Registration

Cron expressions are validated when the trigger is created, not during execution. This fails fast and avoids runtime surprises.

## Future Extensibility

- **New trigger types** – Add `EventTrigger`, `CalendarTrigger`, etc. by subclassing `Trigger`.
- **Alternative planners** – Implement priority‑based, load‑balanced, or distributed planners.
- **Persistence** – Extend `JobRegistry` to use a database or file storage.
- **Distributed scheduling** – Support multiple scheduler instances with leader election.

## Security Considerations

- Job metadata must not contain secrets. Use the `SecretsProvider` for sensitive data.
- Job and workflow names should be validated against injection attacks.
- The scheduler should not execute untrusted workflows; all workflows must be registered and validated.

## Performance Considerations

- The scheduler loop checks due jobs every `interval` seconds (default: 10).
- The registry uses `RLock` for thread‑safe operations.
- Job execution is synchronous; the scheduler does not perform concurrent execution of the same job.
