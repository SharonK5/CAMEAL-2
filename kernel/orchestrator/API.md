# CAMEAL Kernel Orchestrator API

**Package:** `cameal.kernel.orchestrator`

**Version:** 1.0.0

**API Status:** Stable

---

# Overview

The Orchestrator is the execution coordinator of the CAMEAL Kernel.

It transforms an incoming request into an executable workflow by coordinating routing, planning, validation, execution, and response construction.

The Orchestrator **never performs business logic**. It delegates all domain-specific work to registered engines.

---

# Public API

The following classes constitute the stable public API.

| Class | Purpose | Stability |
|---------|----------|-----------|
| `Orchestrator` | Main execution coordinator | Stable |
| `ExecutionPlan` | Immutable workflow plan | Stable |
| `Pipeline` | Ordered execution pipeline | Stable |
| `ExecutionResult` | Final execution result | Stable |
| `OrchestratorError` | Base exception | Stable |

Everything else should be treated as internal implementation detail.

---

# Orchestrator

## Constructor

```python
Orchestrator(
    workflow_manager,
    engine_manager,
    validator=None,
    router=None,
    planner=None,
    executor=None,
    dispatcher=None
)
```

### Parameters

| Parameter | Description |
|------------|-------------|
| workflow_manager | Provides registered workflows |
| engine_manager | Provides registered engines |
| validator | Optional execution validator |
| router | Optional workflow router |
| planner | Optional execution planner |
| executor | Optional pipeline executor |
| dispatcher | Optional engine dispatcher |

---

## execute()

Execute a request.

```python
response = orchestrator.execute(request)
```

### Parameters

| Name | Type |
|------|------|
| request | Request |

### Returns

```python
Response
```

### Process

Execution consists of:

1. Validate request
2. Select workflow
3. Create execution plan
4. Validate plan
5. Execute pipeline
6. Build response

---

## validate()

Validate an execution plan.

```python
orchestrator.validate(plan)
```

Raises

```
ValidationError
```

if the plan is invalid.

---

## health()

Return orchestrator health.

```python
status = orchestrator.health()
```

Returns

```python
HealthStatus
```

---

## execution_plan()

Create an execution plan.

```python
plan = orchestrator.execution_plan(request)
```

Returns

```python
ExecutionPlan
```

This method performs planning only.

No execution occurs.

---

# ExecutionPlan

Represents an immutable execution graph.

```python
ExecutionPlan(
    workflow,
    stages
)
```

## Properties

| Property | Description |
|-----------|-------------|
| workflow | Selected workflow |
| stages | Ordered execution stages |

Example

```python
[
    SecurityEngine,
    RetrievalEngine,
    ReasoningEngine,
    MonitoringEngine,
    EvaluationEngine,
    AccountabilityEngine,
    LearningEngine,
    AdaptationEngine,
]
```

Execution plans are immutable.

---

# Pipeline

Represents executable stages.

```python
Pipeline(plan)
```

Methods

```python
pipeline.next()

pipeline.has_next()

pipeline.reset()

pipeline.current()
```

---

# ExecutionResult

Returned by the Executor.

Properties

| Property | Description |
|-----------|-------------|
| context | Final execution context |
| response | Generated response |
| metrics | Runtime metrics |
| trace | Execution trace |
| success | Execution status |

---

# Exceptions

## OrchestratorError

Base exception.

---

## RoutingError

Workflow selection failed.

---

## PlanningError

Execution plan generation failed.

---

## ExecutionError

Pipeline execution failed.

---

## DispatchError

Engine dispatch failed.

---

## ValidationError

Execution plan validation failed.

---

# Execution Lifecycle

The orchestrator follows the standard kernel lifecycle.

```
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

↓

dispose()
```

---

# Thread Safety

The Orchestrator is stateless.

It contains no mutable execution state.

Every request creates an independent execution context.

This allows concurrent execution without synchronization.

---

# Extension Points

The orchestrator can be extended by replacing:

- Router
- Planner
- Dispatcher
- Executor
- Validator

Custom implementations must preserve the public contracts.

---

# Semantic Versioning

The public API follows Semantic Versioning.

```
MAJOR.MINOR.PATCH
```

Example

```
1.0.0
```

Compatibility rules

| Change | Version |
|----------|----------|
| Bug fixes | PATCH |
| New backwards-compatible features | MINOR |
| Breaking API changes | MAJOR |

---

# Stable Public Contracts

The following classes are guaranteed to remain backwards compatible within major versions.

- Orchestrator
- ExecutionPlan
- Pipeline
- ExecutionResult

---

# Internal API

The following components are implementation details and may change without notice.

- Router
- Planner
- Dispatcher
- Executor
- Validator

Applications should never depend directly on these classes.

---

# Example

```python
from cameal.kernel.orchestrator import Orchestrator

orchestrator = Orchestrator(
    workflow_manager,
    engine_manager,
)

response = orchestrator.execute(request)

print(response)
```

---

# Design Principles

The Orchestrator adheres to the following principles:

- Coordinates execution only.
- Contains no domain intelligence.
- Delegates all work to engines.
- Produces immutable execution plans.
- Executes deterministic workflows.
- Preserves execution context across stages.
- Provides full traceability and observability.
- Remains stateless and thread-safe.
```
