# CAMEAL Kernel Orchestrator – Execution Flow

## Overview

The Orchestrator is the runtime coordinator of the CAMEAL Kernel.

It executes workflows by selecting the appropriate workflow, building an execution
plan, dispatching execution to registered engines, propagating immutable execution
context, and assembling the final response.

The Orchestrator performs **no domain logic**. It only coordinates execution.

---

# High-Level Execution Flow

```
Incoming Request
        │
        ▼
Context Manager
(Build Execution Context)
        │
        ▼
Workflow Router
(Select Workflow)
        │
        ▼
Planner
(Build Execution Plan)
        │
        ▼
Pipeline Validator
(Validate Plan)
        │
        ▼
Executor
(Execute Plan)
        │
        ▼
Dispatcher
(Route to Engine)
        │
        ▼
Engine
(Process Context)
        │
        ▼
Updated Context
        │
        ▼
Next Pipeline Stage
        │
       ...
        │
        ▼
Response Builder
        │
        ▼
Outgoing Response
```

---

# Detailed Execution Sequence

## 1. Request Reception

The Kernel receives a request and delegates execution to the Orchestrator.

Example

```python
response = orchestrator.execute(request)
```

The request is immutable for the lifetime of execution.

---

## 2. Context Construction

The Context Manager creates an immutable `ExecutionContext`.

The context contains:

- Request
- Identity
- Security Context
- Workflow Context
- Provenance Context
- Trace Context
- Metadata

Output

```
ExecutionContext
```

---

## 3. Workflow Selection

The Router determines which workflow should execute.

Example

```
Question Answering
        │
        ▼
QA Workflow
```

or

```
Policy Review
        │
        ▼
Policy Workflow
```

Only one workflow is selected.

---

## 4. Planning

The Planner converts the workflow into an execution plan.

Example

```
Workflow

↓

[
    Security,
    Retrieval,
    Reasoning,
    Monitoring,
    Evaluation,
    Accountability,
    Learning,
    Adaptation
]
```

The execution plan is immutable.

---

## 5. Plan Validation

Before execution begins, the Validator checks:

- workflow exists
- execution order is valid
- no duplicate mandatory stages
- no cycles
- every referenced engine exists

If validation fails, execution stops.

---

## 6. Pipeline Execution

The Executor processes stages sequentially.

```
for stage in plan:
    context = dispatcher.dispatch(stage, context)
```

The Executor never performs business logic.

---

## 7. Engine Dispatch

The Dispatcher resolves the correct engine.

```
EngineManager
        │
        ▼
Retrieve Engine
        │
        ▼
engine.execute(context)
```

The Dispatcher knows **which** engine to invoke, but never **how** it works.

---

## 8. Engine Execution

Each engine receives an immutable context.

```
Input Context
        │
        ▼
Engine
        │
        ▼
Output Context
```

The engine returns a **new** context.

The original context remains unchanged.

---

## 9. Context Propagation

After every stage

```
Old Context
      │
      ▼
Engine
      │
      ▼
New Context
```

The new context becomes input for the next stage.

---

## 10. Response Construction

After the final stage completes

```
Execution Context
        │
        ▼
Response Builder
        │
        ▼
Response
```

The Response contains:

- output
- provenance
- evidence
- trace identifiers
- execution metadata

---

# Complete Runtime Pipeline

```
Request
   │
   ▼
Execution Context
   │
   ▼
Workflow Router
   │
   ▼
Planner
   │
   ▼
Validator
   │
   ▼
Executor
   │
   ▼
Dispatcher
   │
   ▼
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
   │
   ▼
Response Builder
   │
   ▼
Response
```

---

# Context Flow

The execution context is the only object propagated through the pipeline.

```
Context₀
   │
   ▼
Security
   │
   ▼
Context₁
   │
   ▼
Retrieval
   │
   ▼
Context₂
   │
   ▼
Reasoning
   │
   ▼
Context₃
   │
   ▼
...
   │
   ▼
Final Context
```

Each engine produces a new immutable context.

---

# Event Flow

The Orchestrator publishes lifecycle events throughout execution.

```
ExecutionStarted
        │
        ▼
WorkflowSelected
        │
        ▼
StageStarted
        │
        ▼
StageCompleted
        │
        ▼
StageStarted
        │
        ▼
StageCompleted
        │
       ...
        │
        ▼
ExecutionCompleted
```

On failure:

```
ExecutionStarted
        │
        ▼
StageStarted
        │
        ▼
ExecutionFailed
```

---

# Failure Flow

If any stage raises an exception:

```
Current Stage
      │
      ▼
Exception
      │
      ▼
Execution Failed Event
      │
      ▼
Trace Recorded
      │
      ▼
Error Response
```

No remaining stages are executed unless the workflow explicitly supports recovery.

---

# Retry Flow (Optional)

Certain engines may support retry policies.

```
Stage
 │
 ▼
Failure
 │
 ▼
Retry Policy
 │
 ├── Retry
 │
 ▼
Success
 │
 ▼
Continue
```

Retry behavior is defined by workflow policy, not by the Orchestrator.

---

# Parallel Execution (Future)

Future workflow definitions may identify independent stages that can execute concurrently.

```
          Planner
             │
             ▼
      ┌─────────────┐
      │             │
      ▼             ▼
 Retrieval      Monitoring
      │             │
      └──────┬──────┘
             ▼
        Evaluation
             │
             ▼
         Response
```

Parallel scheduling is the responsibility of the Executor, while preserving deterministic output.

---

# Execution Guarantees

The Orchestrator guarantees:

- deterministic workflow execution
- immutable execution context
- ordered stage execution
- validated execution plans
- complete traceability
- provenance propagation
- engine isolation
- fail-fast execution
- reproducible orchestration
- end-to-end observability

---

# Responsibilities

The Orchestrator is responsible for:

- selecting workflows
- building execution plans
- validating execution plans
- dispatching execution
- propagating execution context
- coordinating engines
- assembling responses
- publishing execution events

---

# Non-Responsibilities

The Orchestrator never:

- performs reasoning
- retrieves evidence
- evaluates policies
- invokes LLM prompts directly
- executes machine learning models
- stores domain data
- authenticates users
- authorizes requests
- implements business rules
- mutates repository state directly

These responsibilities belong to their respective engines and repositories.

---

# Summary

The Orchestrator is the execution coordinator of the CAMEAL Kernel. It transforms an incoming request into a validated execution plan, coordinates engine execution through immutable context propagation, and produces a fully traceable response. By separating orchestration from domain intelligence, it provides deterministic, observable, extensible, and maintainable runtime behavior.
