# CAMEAL Kernel Managers API

**Package:** `cameal.kernel.managers`

**Version:** 1.0.0

---

# Overview

The Managers subsystem provides the runtime coordination layer of the CAMEAL Kernel.

Managers own and coordinate runtime components but **never implement domain logic**. They expose a stable API used by the Kernel while hiding the implementation details of engines, repositories, workflows, plugins, schedulers, and execution contexts.

The public API follows semantic versioning. Only documented public classes are guaranteed to remain stable across minor releases.

---

# Public API

The following classes are part of the stable public API.

| Class | Responsibility | Stability |
|---------|---------------|-----------|
| `Manager` | Base manager interface | Stable |
| `EngineManager` | Manages runtime engines | Stable |
| `RepositoryManager` | Manages repositories | Stable |
| `WorkflowManager` | Manages workflow definitions | Stable |
| `ContextManager` | Manages execution contexts | Stable |
| `PluginManager` | Manages plugins | Stable |
| `SchedulerManager` | Manages scheduled jobs | Stable |

---

# Internal API

The following components are internal implementation details.

These components **must not** be used directly by plugins.

- Registry
- Validator
- Resolution algorithms
- Dependency graph
- Internal caches
- Discovery helpers

These may change without notice.

---

# Base Manager

All managers inherit from the common Manager interface.

```python
class Manager:
    initialize() -> None
    validate() -> None
    start() -> None
    stop() -> None
    shutdown() -> None
    health() -> HealthStatus
```

Every manager follows the Kernel lifecycle.

---

# EngineManager

Coordinates all runtime engines.

## Responsibilities

- register engines
- unregister engines
- resolve engines
- start engines
- stop engines
- health aggregation

## Public Methods

```python
register(engine)

unregister(name)

get(name)

list()

start_all()

stop_all()

health()
```

---

# RepositoryManager

Coordinates domain repositories.

## Responsibilities

- register repositories
- resolve repositories
- validate repositories
- lifecycle management

## Public Methods

```python
register(repository)

get(name)

list()

validate()

health()
```

---

# WorkflowManager

Coordinates executable workflows.

## Responsibilities

- workflow registration
- workflow lookup
- workflow validation
- workflow execution

## Public Methods

```python
register(workflow)

execute(name, context)

list()

validate()

health()
```

---

# ContextManager

Coordinates runtime execution contexts.

## Responsibilities

- create execution contexts
- update contexts
- propagate contexts
- destroy contexts

## Public Methods

```python
create(request)

get(context_id)

update(context)

remove(context_id)

health()
```

---

# PluginManager

Coordinates runtime plugins.

## Responsibilities

- discover plugins
- validate manifests
- load plugins
- unload plugins
- dependency resolution

## Public Methods

```python
discover()

load()

unload()

reload()

list()

health()
```

---

# SchedulerManager

Coordinates scheduled background work.

## Responsibilities

- register jobs
- schedule jobs
- cancel jobs
- execute recurring jobs

## Public Methods

```python
schedule(job)

cancel(job)

pause(job)

resume(job)

list()

health()
```

---

# Manager Lifecycle

Every manager follows the same lifecycle.

```
initialize()

↓

validate()

↓

boot()

↓

start()

↓

running

↓

stop()

↓

shutdown()

↓

dispose()
```

Managers may only expose public functionality while in the **Running** state.

---

# Error Handling

Managers raise only typed exceptions.

| Exception | Description |
|-----------|-------------|
| `ManagerError` | Base manager exception |
| `RegistrationError` | Registration failed |
| `ValidationError` | Validation failed |
| `ResolutionError` | Lookup failed |
| `LifecycleError` | Invalid lifecycle transition |

Managers never return partially initialized components.

---

# Thread Safety

Managers are designed to be thread-safe.

Guarantees include:

- atomic registration
- atomic removal
- immutable runtime metadata
- synchronized lifecycle transitions
- lock-protected registries where required

---

# Runtime Guarantees

The Managers subsystem guarantees:

- deterministic component registration
- immutable component identity
- lifecycle consistency
- dependency isolation
- thread-safe coordination
- health aggregation
- component discoverability

---

# Extension Model

Plugins may register new:

- Engines
- Repositories
- Workflows
- Scheduled Jobs

Plugins **cannot** replace or modify Kernel managers.

Managers remain the authoritative coordinators for their respective runtime domains.

---

# Versioning

## Stable Public API

- Manager
- EngineManager
- RepositoryManager
- WorkflowManager
- ContextManager
- PluginManager
- SchedulerManager

These follow semantic versioning.

---

## Internal API

The following components are internal and may change without notice:

- Registry
- Validator
- Discovery algorithms
- Internal caches
- Resolution algorithms

---

# Example

```python
from cameal.kernel.managers import EngineManager

manager = EngineManager()

manager.register(reasoning_engine)
manager.register(security_engine)

manager.start_all()

engine = manager.get("reasoning")

response = engine.execute(context)

manager.stop_all()
```

---

# API Stability

| Component | Status |
|------------|--------|
| Public API | Stable |
| Internal API | Private |
| Semantic Versioning | Enabled |
| Thread Safety | Guaranteed |
| Lifecycle Compatible | Yes |
| Plugin Safe | Yes |
