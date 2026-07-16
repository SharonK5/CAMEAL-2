# CAMEAL Services

## Overview

The `services` subsystem provides the implementation layer for CAMEAL.

Execution stages orchestrate workflow, while services perform the actual
business logic.

This separation ensures that execution remains lightweight and that domain
logic can evolve independently of workflow orchestration.

```
Execution Stage
        │
        ▼
     Service
        │
        ▼
 Domain Logic
        │
        ▼
Repositories / AI / External Systems
```

---

## Responsibilities

Services are responsible for:

- Domain-specific computation
- Analytics
- Monitoring
- Evaluation
- Accountability
- Learning
- Adaptation
- Retrieval
- LLM interaction
- Enterprise integrations

Services never determine execution order.

Execution stages coordinate services.

---

## Design Principles

- Single responsibility
- Stateless where possible
- Dependency injection
- Interface-first design
- Testability
- Extensibility
- Governance-first execution

---

## Planned Modules

```
services/

analytics/
monitoring/
evaluation/
accountability/
learning/
adaptation/

rag/
llm/
enterprise/
```

Each module may expose:

- Service
- Manager
- Registry
- Factory
- Builder
- Contracts

---

## Relationship to Execution

Execution stages invoke services.

Example:

```
AnalyticsStage
        │
        ▼
AnalyticsService
        │
        ▼
Climate Analyzer
Evidence Analyzer
Gap Analyzer
Confidence Analyzer
```

Stages orchestrate.

Services implement.

---

## Status

Current Status:

- Foundation
- Service abstraction
- Registry
- Resolver
- Builder
- Manager

Future:

- Domain Services
- AI Services
- Enterprise Services
