# CAMEAL Kernel Managers

## Overview

The **Managers** subsystem provides the orchestration layer of the CAMEAL Kernel.

Managers coordinate runtime components but **never implement domain intelligence**. They are responsible for discovering, registering, supervising, and coordinating the major runtime subsystems that together form the execution environment.

Managers serve as the operational backbone of the kernel by ensuring that engines, repositories, plugins, workflows, schedulers, and execution contexts operate as a coherent runtime.

---

# Design Goals

The Managers subsystem is designed around six principles:

1. **Centralized coordination** – every runtime subsystem is managed through a dedicated manager.
2. **Separation of concerns** – managers coordinate; engines execute.
3. **Lifecycle supervision** – managers initialize, start, monitor, and stop managed components.
4. **Dependency isolation** – managers resolve dependencies through the kernel container.
5. **Extensibility** – new managers may be introduced without modifying existing ones.
6. **Observability** – managers expose health, diagnostics, metrics, and execution status.

---

# Responsibilities

Managers are responsible for:

- registering runtime components
- lifecycle coordination
- dependency resolution
- runtime supervision
- workflow selection
- repository coordination
- plugin management
- execution context coordination
- scheduler coordination
- diagnostics and health reporting

Managers **never** perform business logic.

---

# Managed Runtime Components

The subsystem manages:

- Engine Manager
- Repository Manager
- Workflow Manager
- Context Manager
- Plugin Manager
- Scheduler Manager

Each manager owns exactly one runtime concern.

---

# Runtime Architecture

```text
                        Kernel
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
 Engine Manager    Repository Manager   Workflow Manager
        │                  │                  │
        ▼                  ▼                  ▼
     Engines         Repositories       Workflows

                           │
                           ▼
                   Context Manager
                           │
                           ▼
                    Execution Context

                           │
                           ▼
                    Scheduler Manager
                           │
                           ▼
                     Scheduled Tasks

                           │
                           ▼
                     Plugin Manager
                           │
                           ▼
                Plugins / Extensions
```

---

# Manager Responsibilities

## Engine Manager

Responsible for:

- engine discovery
- engine registration
- engine initialization
- engine lifecycle
- engine health
- engine execution routing

The Engine Manager never performs reasoning or monitoring itself.

---

## Repository Manager

Responsible for:

- repository discovery
- repository registration
- repository resolution
- repository health
- repository configuration

Repositories own persistent state.

---

## Workflow Manager

Responsible for:

- workflow discovery
- workflow selection
- workflow execution
- workflow validation
- workflow registration

Workflows define execution order but contain no business logic.

---

## Context Manager

Responsible for:

- execution context creation
- propagation
- context updates
- trace management
- provenance propagation

Contexts remain immutable throughout execution.

---

## Plugin Manager

Responsible for:

- plugin discovery
- manifest validation
- dependency validation
- plugin loading
- plugin activation
- plugin unloading

Plugins extend runtime capabilities without modifying the kernel.

---

## Scheduler Manager

Responsible for:

- scheduled jobs
- periodic tasks
- timers
- background execution
- maintenance tasks

Typical scheduled work includes:

- learning cycles
- repository indexing
- health checks
- cleanup
- audits

---

# Runtime Execution Flow

```text
Kernel
   │
   ▼
Managers
   │
   ├──────── Engine Manager
   │
   ├──────── Repository Manager
   │
   ├──────── Workflow Manager
   │
   ├──────── Context Manager
   │
   ├──────── Plugin Manager
   │
   └──────── Scheduler Manager
            │
            ▼
      Runtime Components
```

---

# Manager Lifecycle

Every manager follows the kernel lifecycle:

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

↓

dispose()
```

Managers are supervised by the Kernel Lifecycle subsystem.

---

# Runtime Guarantees

The Managers subsystem guarantees:

- deterministic coordination
- dependency isolation
- lifecycle consistency
- manager independence
- plugin compatibility
- execution traceability
- health aggregation
- runtime extensibility

---

# Public API

The stable public API consists of:

- Manager
- EngineManager
- RepositoryManager
- WorkflowManager
- ContextManager
- PluginManager
- SchedulerManager

These classes follow semantic versioning.

---

# Internal Components

Internal implementation classes include:

- Registry
- Validator
- Resolver
- Factory
- Diagnostics
- Utilities

These are **not** considered stable public APIs and may change between minor releases.

---

# What Managers Do Not Do

Managers never:

- perform reasoning
- retrieve knowledge
- evaluate policies
- execute machine learning
- call LLMs
- perform monitoring
- evaluate evidence
- perform learning
- adapt system behaviour

These responsibilities belong exclusively to the corresponding engines.

---

# Relationship to Other Kernel Subsystems

```text
                    Bootstrap
                         │
                         ▼
                    Container
                         │
                         ▼
                     Managers
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
   Events             Context          Lifecycle
                         │
                         ▼
                   Runtime Engines
```

Managers coordinate all runtime components while relying on the Container for dependency resolution, the Lifecycle subsystem for state transitions, the Events subsystem for asynchronous communication, and the Context subsystem for execution state propagation.

---

# Version

Current Version: **1.0.0**

API Status: **Stable**

Compatibility: **Semantic Versioning**
