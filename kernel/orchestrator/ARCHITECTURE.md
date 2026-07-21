# CAMEAL Kernel Orchestrator – Architecture

## Overview

The **Orchestrator** is the execution coordinator of the CAMEAL Kernel.

It is responsible for transforming an incoming request into an executable workflow, coordinating execution across registered engines, propagating execution context, and returning the final response.

The orchestrator contains **no domain intelligence**. It never performs retrieval, reasoning, monitoring, evaluation, learning, or adaptation itself. Those responsibilities belong exclusively to the respective engines.

---

# Architectural Principles

The orchestrator is built around the following principles:

1. **Pure orchestration**
   - Coordinates execution only.
   - Never implements business logic.

2. **Workflow-driven execution**
   - All execution follows workflow definitions.
   - Execution order is deterministic.

3. **Immutable execution context**
   - Context flows through every stage.
   - Engines return updated contexts rather than mutating shared state.

4. **Loose coupling**
   - Engines never call one another directly.
   - Communication is mediated through the orchestrator.

5. **Stateless coordination**
   - The orchestrator maintains no request state.
   - State exists only inside ExecutionContext.

---

# Internal Architecture

```text
                       ┌────────────────────────────┐
                       │        Orchestrator        │
                       │        (Public API)        │
                       └─────────────┬──────────────┘
                                     │
             ┌───────────────────────┼───────────────────────┐
             │                       │                       │
             ▼                       ▼                       ▼
     ┌──────────────┐       ┌────────────────┐      ┌────────────────┐
     │    Router    │       │    Planner     │      │   Validator    │
     └──────┬───────┘       └──────┬─────────┘      └────────────────┘
            │                      │
            ▼                      ▼
                  ┌─────────────────────────────┐
                  │      Execution Plan         │
                  │     (Immutable Pipeline)    │
                  └─────────────┬───────────────┘
                                │
                                ▼
                      ┌─────────────────────┐
                      │      Executor       │
                      └─────────┬───────────┘
                                │
                                ▼
                      ┌─────────────────────┐
                      │     Dispatcher      │
                      └─────────┬───────────┘
                                │
                                ▼
                     Registered Kernel Engines
```

---

# Architectural Layers

## 1. Public Layer

The public interface is the `Orchestrator`.

Responsibilities:

- execute requests
- validate workflows
- expose runtime health

Only this layer is consumed by the kernel.

---

## 2. Routing Layer

Implemented by the Router.

Responsibilities:

- determine workflow
- select execution strategy
- resolve workflow identifiers

No execution occurs here.

---

## 3. Planning Layer

Implemented by the Planner.

Responsibilities:

- convert workflow into execution plan
- determine engine order
- build immutable pipeline

Produces an ExecutionPlan object.

---

## 4. Validation Layer

Implemented by Validator.

Responsibilities:

- workflow validation
- engine availability
- duplicate detection
- dependency verification
- execution integrity

Validation always occurs before execution.

---

## 5. Execution Layer

Implemented by Executor.

Responsibilities:

- execute engines sequentially
- propagate context
- stop on unrecoverable failures
- collect outputs

Executor never chooses engines.

---

## 6. Dispatch Layer

Implemented by Dispatcher.

Responsibilities:

- locate engine
- invoke engine
- return updated context

Dispatcher performs no orchestration.

---

# Runtime Component Relationships

```text
Kernel
   │
   ▼
Orchestrator
   │
   ├────────► WorkflowManager
   │
   ├────────► EngineManager
   │
   ├────────► ContextManager
   │
   └────────► EventBus
```

The orchestrator depends only on runtime managers.

It never communicates directly with repositories or providers.

---

# Execution Pipeline

```text
Request
   │
   ▼
Context Builder
   │
   ▼
Workflow Selection
   │
   ▼
Execution Planning
   │
   ▼
Validation
   │
   ▼
Pipeline Execution
   │
   ▼
Engine Dispatch
   │
   ▼
Updated Context
   │
   ▼
Next Engine
   │
   ▼
Response Builder
   │
   ▼
Response
```

---

# Engine Coordination

The orchestrator coordinates engines but never interprets their outputs.

Example pipeline:

```text
Security Engine
        │
        ▼
Retrieval Engine
        │
        ▼
Reasoning Engine
        │
        ▼
Monitoring Engine
        │
        ▼
Evaluation Engine
        │
        ▼
Accountability Engine
        │
        ▼
Learning Engine
        │
        ▼
Adaptation Engine
```

Each engine receives an immutable ExecutionContext.

Each engine returns a new ExecutionContext.

---

# Dependency Relationships

```text
Orchestrator
     │
     ├── EngineManager
     ├── WorkflowManager
     ├── ContextManager
     ├── EventBus
     └── Container
```

No dependency exists on:

- repositories
- providers
- plugins
- storage

These are accessed indirectly through managers or engines.

---

# Context Propagation

ExecutionContext is the only object shared between stages.

```text
Context₀
   │
Security
   │
Context₁
   │
Retrieval
   │
Context₂
   │
Reasoning
   │
Context₃
   │
...
```

Contexts are immutable.

Each stage produces a new context.

---

# Failure Handling

Failures terminate the active pipeline.

```text
Request
   │
Security
   │
Retrieval
   │
Reasoning
   │
Exception
   │
Failure Response
```

The orchestrator:

- records failure
- emits failure events
- stops execution
- returns structured error response

Recovery logic belongs to workflows or engines.

---

# Thread Safety

The orchestrator is stateless.

Therefore it is naturally thread-safe.

Per-request state exists only within:

- ExecutionContext
- Request
- Response

Concurrent executions never share mutable state.

---

# Event Integration

The orchestrator publishes lifecycle events.

Typical events include:

```text
WorkflowStarted

WorkflowCompleted

WorkflowFailed

EngineStarted

EngineCompleted

EngineFailed
```

The orchestrator does not subscribe to domain events.

---

# Design Constraints

The orchestrator MUST NOT:

- perform reasoning
- retrieve knowledge
- evaluate policies
- execute ML models
- call LLMs directly
- access repositories
- mutate shared state

It coordinates execution only.

---

# Public vs Internal API

## Stable Public API

- Orchestrator
- ExecutionPlan

These follow semantic versioning.

---

## Internal Components

The following are implementation details and may change without notice:

- Planner
- Router
- Executor
- Dispatcher
- Validator

Applications should never depend on them directly.

---

# Extensibility

New execution behavior is introduced by:

- registering new workflows
- registering new engines
- extending planners
- extending routers

The orchestrator itself is never modified to support domain capabilities.

---

# Architectural Summary

| Component | Responsibility |
|----------|----------------|
| Orchestrator | Coordinates execution |
| Router | Selects workflow |
| Planner | Builds execution plan |
| Validator | Validates plan |
| Executor | Executes pipeline |
| Dispatcher | Invokes engines |
| EngineManager | Resolves engines |
| WorkflowManager | Resolves workflows |
| ContextManager | Builds execution context |
| EventBus | Publishes runtime events |

---

# Architecture Guarantees

The orchestrator guarantees:

- deterministic execution
- immutable context propagation
- stateless coordination
- workflow-driven execution
- engine isolation
- validated execution plans
- complete traceability
- end-to-end observability
- explainable orchestration
- thread-safe concurrent execution
```
