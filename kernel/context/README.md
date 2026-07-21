# CAMEAL Kernel Context

## Overview

The **Kernel Context** subsystem provides the execution context for every request processed by the CAMEAL runtime.

It is responsible for creating, validating, propagating, and managing immutable execution context as requests move through the kernel and the engine pipeline.

The Context subsystem is **the shared state carrier of the runtime**. It enables secure, deterministic, explainable, and traceable execution without allowing engines to share mutable state.

The Context subsystem contains **no business logic**. It only carries execution state.

---

# Design Goals

The Context subsystem is designed around six principles.

1. **Immutable execution state**
2. **Complete traceability**
3. **Separation of runtime from domain state**
4. **Deterministic execution**
5. **Explainable processing**
6. **Safe context propagation**

---

# Responsibilities

| Responsibility | Description |
|---------------|-------------|
| Context Creation | Creates execution contexts for incoming requests |
| Context Validation | Validates context integrity |
| Context Propagation | Passes context through every engine |
| Trace Management | Maintains request tracing |
| Provenance Tracking | Carries evidence lineage |
| Workflow State | Maintains execution progress |
| Security Context | Carries identity and authorization metadata |
| Request Metadata | Stores runtime metadata |
| Diagnostics Support | Supplies tracing and metrics information |

---

# What the Context Subsystem Does NOT Do

The Context subsystem does **not** perform:

- Authentication
- Authorization
- Policy Evaluation
- Retrieval
- Reasoning
- Machine Learning
- RAG
- LLM Prompting
- Monitoring
- Evaluation
- Learning
- Adaptation

These responsibilities belong to their respective engines.

---

# Core Context Types

The subsystem manages multiple specialized contexts.

| Context | Purpose |
|----------|---------|
| ExecutionContext | Overall runtime state |
| RequestContext | Request metadata |
| SecurityContext | Identity, roles, permissions |
| WorkflowContext | Current workflow state |
| TraceContext | Distributed tracing |
| ProvenanceContext | Evidence lineage |

---

# Context Lifecycle

Every request creates a new immutable execution context.

```
Incoming Request
        │
        ▼
Create Execution Context
        │
        ▼
Validate
        │
        ▼
Attach Trace Information
        │
        ▼
Attach Security Context
        │
        ▼
Attach Workflow Context
        │
        ▼
Propagate Through Engines
        │
        ▼
Return Final Context
```

Each engine receives an immutable context and produces a new derived context.

---

# Runtime Flow

```
Request

      │

      ▼

Execution Context

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

Response
```

The context accompanies every stage of execution.

---

# Context Ownership

The Context subsystem owns only runtime state.

| State | Owner |
|---------|-------|
| Identity | Security Context |
| Trace IDs | Trace Context |
| Workflow Status | Workflow Context |
| Evidence Provenance | Provenance Context |
| Runtime Metadata | Request Context |

Domain objects remain inside repositories.

---

# Immutability

Contexts are immutable.

Instead of modifying context,

```
Context A

↓

Engine

↓

Context B
```

This enables:

- deterministic execution
- replay
- auditability
- thread safety
- distributed execution

---

# Runtime Guarantees

The Context subsystem guarantees:

- immutable execution state
- deterministic propagation
- end-to-end traceability
- provenance preservation
- thread safety
- engine isolation
- workflow consistency
- reproducible execution

---

# Extension Model

Additional context types may be added as plugins.

Examples include:

- TenantContext
- SessionContext
- GeoContext
- ComplianceContext
- ExperimentContext
- SimulationContext

The Kernel automatically propagates registered context types.

---

# Example

```python
from cameal.kernel.context import ExecutionContext

context = ExecutionContext(
    request_id="REQ-1001",
    trace_id="TRACE-abc123",
    workflow="policy_review"
)

response = kernel.execute(request, context)
```

---

# Relationship to Other Kernel Components

```
Kernel
   │
   ├── Container
   ├── Lifecycle
   ├── Events
   ├── Context
   ├── Managers
   ├── Scheduler
   └── Orchestrator
```

The Context subsystem is shared by every runtime component.

---

# Version

Current Version

**1.0.0**

Public API Status

**Stable**
