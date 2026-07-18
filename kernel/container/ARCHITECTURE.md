# CAMEAL Kernel Container – Architecture

## Purpose

The Container is the dependency injection subsystem of the CAMEAL Kernel.

It is responsible for constructing runtime objects, resolving dependencies,
managing object lifetimes, and providing dependency inversion across the
platform.

The container contains **no business logic** and performs **no workflow
execution**.

---

# Architectural Goals

The architecture is designed to achieve:

- Loose coupling
- Dependency inversion
- Constructor injection
- Type-safe resolution
- Deterministic object construction
- Thread-safe singleton management
- Request isolation
- Extensibility
- High testability

---

# Internal Architecture

```
┌──────────────────────────────────────────────┐
│                 Container                    │
│          (Public Dependency API)             │
└───────────────────┬──────────────────────────┘
                    │
     ┌──────────────┼───────────────┐
     │              │               │
     ▼              ▼               ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│Registration│ │ Resolver   │ │ Validator  │
└─────┬──────┘ └─────┬──────┘ └────────────┘
      │              │
      ▼              ▼
┌────────────┐ ┌────────────┐
│ Registry   │ │ Injector   │
└─────┬──────┘ └─────┬──────┘
      │              │
      └──────┬───────┘
             ▼
      ┌────────────┐
      │   Cache    │
      └─────┬──────┘
            ▼
      ┌────────────┐
      │  Scopes    │
      └────────────┘
```

---

# Layer Responsibilities

## Public API

Provides dependency registration and resolution.

Primary component:

- Container

---

## Registration Layer

Responsible for creating dependency registrations.

Components:

- Registration
- Dependency

---

## Registry Layer

Maintains the complete dependency graph.

Responsibilities:

- Store registrations
- Lookup registrations
- Freeze registrations after bootstrap

---

## Resolution Layer

Responsible for resolving dependencies recursively.

Components:

- Resolver
- Injector

The Resolver consults the Validator before constructing dependency graphs.

---

## Validation Layer

Responsible for validating the dependency graph.

Checks include:

- Missing registrations
- Circular dependencies
- Invalid scopes
- Duplicate registrations
- Constructor compatibility

---

## Cache Layer

Maintains runtime instances.

Supports:

- Singleton cache
- Request cache

Transient instances are never cached.

---

## Scope Layer

Defines object lifetimes.

Supported scopes:

- Singleton
- Request
- Transient

---

# Dependency Resolution Flow

1. Register dependency.
2. Create registration.
3. Store registration.
4. Resolve requested type.
5. Validate dependency graph.
6. Check cache.
7. Resolve constructor parameters recursively.
8. Construct instance.
9. Cache instance if required.
10. Return instance.

---

# Constructor Injection

The container supports **constructor injection only**.

Dependencies are resolved using constructor type annotations.

Field injection and property injection are intentionally unsupported.

This guarantees:

- immutable construction
- explicit dependencies
- deterministic object creation
- improved testability

---

# Thread Safety

The container guarantees:

- thread-safe singleton creation
- isolated request scopes
- lock-free transient creation
- immutable registrations after bootstrap

---

# Lifecycle

```
Create Container
        │
        ▼
Register Dependencies
        │
        ▼
Validate Graph
        │
        ▼
Freeze Registrations
        │
        ▼
Resolve Objects
        │
        ▼
Request Begin
        │
        ▼
Request End
        │
        ▼
Kernel Shutdown
```

---

# Design Constraints

The Container SHALL NOT:

- execute workflows
- invoke engines
- manage repositories
- publish events
- perform security decisions
- implement business logic

Its sole responsibility is dependency composition.

---

# Quality Attributes

The architecture provides:

- Determinism
- Thread Safety
- Testability
- Extensibility
- Low Coupling
- High Cohesion
- Dependency Inversion
- Immutable Construction
- Predictable Lifetimes
- Runtime Efficiency
