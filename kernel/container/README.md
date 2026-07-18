# CAMEAL Kernel Container

## Overview

The Container is the dependency injection subsystem of the CAMEAL Kernel.

It is responsible for constructing objects, resolving dependencies, managing
component lifetimes, and ensuring loose coupling between runtime components.

The container does **not** contain business logic and does **not** manage
application workflows. It exists solely to provide object composition for the
runtime.

---

## Responsibilities

The container provides:

- Dependency registration
- Dependency resolution
- Constructor injection
- Lifetime management
- Scoped instances
- Request-scoped caching
- Singleton management
- Circular dependency detection
- Lazy instantiation

---

## Supported Scopes

| Scope | Lifetime |
|--------|----------|
| Singleton | One instance for the lifetime of the kernel |
| Request | One instance per execution request |
| Transient | New instance every resolution |

---

## Resolution Process

```
Request Object
      │
      ▼
Resolve Dependency
      │
      ▼
Lookup Registration
      │
      ▼
Create Dependencies
      │
      ▼
Inject Constructor
      │
      ▼
Return Instance
```

---

## Design Principles

The container follows these principles:

- constructor injection only
- no service locator pattern inside engines
- immutable registrations after kernel startup
- deterministic dependency graph
- type-safe resolution
- lazy object creation
- scope isolation

---

## Public Components

```
Container
Dependency
Scope
```

---

## Usage

```python
from cameal.kernel.container import Container, Scope

container = Container()

container.register(
    Repository,
    SQLRepository,
    Scope.SINGLETON,
)

container.register(
    ReasoningEngine,
    DefaultReasoningEngine,
    Scope.REQUEST,
)

engine = container.resolve(ReasoningEngine)
```

---

## Runtime Guarantees

The container guarantees:

- deterministic resolution
- singleton consistency
- request isolation
- thread-safe singleton access
- circular dependency detection
- constructor validation

---

## What the Container Does Not Do

The container never:

- execute workflows
- call engines
- manage repositories
- evaluate security
- perform reasoning
- process events
- execute plugins

Those responsibilities belong to the Kernel.
