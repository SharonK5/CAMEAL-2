# CAMEAL Kernel Managers – Execution Flow

## Purpose

The Managers subsystem coordinates the runtime infrastructure of the CAMEAL Kernel.

Managers do **not** execute business logic. Instead, they coordinate engines,
repositories, workflows, plugins, scheduling, and runtime context.

The subsystem provides a single orchestration layer between the Kernel and the
runtime components.

---

# Execution Overview

```text
Kernel
   │
   ▼
Manager Layer
   │
   ├───────────────┐
   │               │
   ▼               ▼
EngineManager   RepositoryManager
   │               │
   ▼               ▼
Registered     Domain Repositories
Engines
   │
   ├───────────────┐
   ▼               ▼
WorkflowManager  ContextManager
   │               │
   ▼               ▼
Workflow       Execution Context
Selection      Propagation
   │
   ▼
PluginManager
   │
   ▼
SchedulerManager
   │
   ▼
Execution Pipeline
```

---

# Runtime Sequence

Every request entering the Kernel follows the same management sequence.

```text
Incoming Request
        │
        ▼
ContextManager
        │
        ▼
Create Execution Context
        │
        ▼
WorkflowManager
        │
        ▼
Select Workflow
        │
        ▼
RepositoryManager
        │
        ▼
Resolve Required Repositories
        │
        ▼
EngineManager
        │
        ▼
Resolve Required Engines
        │
        ▼
PluginManager
        │
        ▼
Load Dynamic Extensions
        │
        ▼
SchedulerManager
        │
        ▼
Schedule Background Tasks
        │
        ▼
Execution Pipeline
        │
        ▼
Response
```

---

# Manager Responsibilities During Execution

## 1. ContextManager

Responsibilities

- Create execution context.
- Merge request context.
- Propagate trace information.
- Maintain immutable runtime state.
- Attach provenance.

Produces

```text
ExecutionContext
```

Consumes

```text
Request
Session
Security Context
Workflow Metadata
```

---

## 2. WorkflowManager

Responsibilities

- Identify workflow type.
- Validate workflow.
- Build execution graph.
- Resolve execution order.

Produces

```text
WorkflowGraph
```

Consumes

```text
ExecutionContext
```

---

## 3. RepositoryManager

Responsibilities

- Resolve repositories.
- Validate repository availability.
- Inject repository instances.
- Manage repository lifecycle.

Produces

```text
Repository Set
```

Consumes

```text
WorkflowGraph
```

---

## 4. EngineManager

Responsibilities

- Resolve required engines.
- Verify dependencies.
- Initialize engines.
- Coordinate execution order.

Produces

```text
Engine Execution Plan
```

Consumes

```text
WorkflowGraph
Repository Set
```

---

## 5. PluginManager

Responsibilities

- Discover plugins.
- Validate manifests.
- Register extensions.
- Load providers.
- Register workflows.
- Register repositories.
- Register engines.

Produces

```text
Runtime Extensions
```

Consumes

```text
Plugin Registry
```

---

## 6. SchedulerManager

Responsibilities

- Schedule asynchronous jobs.
- Trigger periodic workflows.
- Execute delayed tasks.
- Monitor scheduled execution.

Produces

```text
Scheduled Tasks
```

Consumes

```text
Execution Plan
```

---

# Execution Dependencies

Managers execute in a deterministic order.

```text
ContextManager
        │
        ▼
WorkflowManager
        │
        ▼
RepositoryManager
        │
        ▼
EngineManager
        │
        ▼
PluginManager
        │
        ▼
SchedulerManager
```

No manager may execute before its dependencies are satisfied.

---

# Interaction with Other Kernel Subsystems

## Container

Managers resolve runtime services using the Dependency Injection Container.

```text
Container
        │
        ▼
Managers
```

---

## Events

Managers publish lifecycle and execution events.

Example

```text
Workflow Selected

Engine Loaded

Repository Resolved

Plugin Registered

Task Scheduled
```

---

## Context

Managers receive immutable execution context and produce updated context.

```text
Context In
      │
      ▼
Manager
      │
      ▼
Context Out
```

Managers never mutate the existing context.

---

## Lifecycle

Managers participate in the kernel lifecycle.

```text
initialize()

↓

validate()

↓

boot()

↓

start()

↓

execute()

↓

stop()

↓

shutdown()
```

---

# Failure Handling

Each manager validates its own execution.

If a manager fails

```text
Manager Failure
       │
       ▼
Publish Event
       │
       ▼
Rollback (if applicable)
       │
       ▼
Raise Runtime Exception
       │
       ▼
Kernel Error Handler
```

Managers do not suppress failures.

---

# Background Execution

Some managers may perform asynchronous work.

Examples

- Plugin discovery
- Learning jobs
- Index rebuilding
- Metrics aggregation
- Health polling
- Scheduled audits

These tasks are delegated to the SchedulerManager.

---

# Concurrency Model

Managers are stateless coordinators.

They should:

- avoid shared mutable state
- rely on immutable execution contexts
- resolve dependencies through the Container
- publish events instead of direct coupling

This allows safe concurrent request processing.

---

# Runtime Guarantees

The Managers subsystem guarantees:

- deterministic orchestration
- immutable context propagation
- dependency-driven execution
- plugin-aware runtime coordination
- repository isolation
- engine lifecycle consistency
- asynchronous task scheduling
- complete execution traceability
- event-driven coordination
- consistent failure propagation

---

# Execution Summary

```text
Request
   │
   ▼
ContextManager
   │
   ▼
WorkflowManager
   │
   ▼
RepositoryManager
   │
   ▼
EngineManager
   │
   ▼
PluginManager
   │
   ▼
SchedulerManager
   │
   ▼
Execution Pipeline
   │
   ▼
Response
```

The Managers subsystem is the operational coordination layer of the CAMEAL Kernel. It transforms incoming requests into a fully prepared execution plan by resolving context, workflows, repositories, engines, plugins, and scheduled tasks before control passes to the execution pipeline. It contains no domain-specific business logic and remains responsible solely for runtime orchestration.
