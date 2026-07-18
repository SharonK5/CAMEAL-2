# CAMEAL Kernel Container Execution Flow

## Overview

The Container is the dependency injection runtime of the CAMEAL Kernel.

It is responsible for constructing, managing, validating, and providing dependencies throughout the lifetime of the application.

The execution flow is deterministic, thread-safe, and lifecycle-aware.

---

# High-Level Flow

```
Bootstrap
    │
    ▼
Create Container
    │
    ▼
Register Dependencies
    │
    ▼
Validate Dependency Graph
    │
    ▼
Freeze Registrations
    │
    ▼
Kernel Boot
    │
    ▼
Begin Request
    │
    ▼
Resolve Dependencies
    │
    ▼
Execute Workflow
    │
    ▼
End Request
    │
    ▼
Dispose Request Scope
    │
    ▼
Kernel Shutdown
```

---

# Phase 1 — Container Construction

The kernel creates an empty container.

```python
container = Container()
```

Responsibilities

- initialize registry
- initialize caches
- initialize validator
- initialize resolver
- initialize injector

At this stage the container contains no registrations.

---

# Phase 2 — Registration

Components register dependencies.

Examples

```python
container.register(
    Repository,
    SqlRepository,
    Scope.SINGLETON,
)
```

```python
container.register(
    ReasoningEngine,
    DefaultReasoningEngine,
    Scope.REQUEST,
)
```

Each registration creates a `Dependency` object and stores it in the registry.

---

# Phase 3 — Validation

Before the kernel starts, the container validates the dependency graph.

Validation includes:

- duplicate registrations
- missing implementations
- invalid scopes
- circular dependencies
- constructor dependency graph

If validation fails:

```
ValidationError
```

is raised and kernel startup stops.

---

# Phase 4 — Freeze

After validation the registration graph becomes immutable.

```
Registrations

READ ONLY
```

No additional registrations are allowed after boot unless explicitly supported through the plugin lifecycle.

This guarantees deterministic execution.

---

# Phase 5 — Request Begins

When the kernel starts processing a request:

```python
container.begin_request()
```

The request cache is created.

```
Request Cache

{}
```

Only request-scoped objects are stored here.

---

# Phase 6 — Resolution

When a dependency is requested:

```python
service = container.resolve(Service)
```

the resolver performs the following steps.

```
Lookup

↓

Registration

↓

Scope

↓

Cache

↓

Constructor Inspection

↓

Recursive Resolution

↓

Object Creation

↓

Cache (if applicable)

↓

Return Instance
```

---

# Constructor Injection

Dependencies are resolved recursively.

Example

```python
class Service:

    def __init__(
        self,
        repository: Repository,
        logger: Logger,
    ):
        ...
```

Execution

```
Resolve(Service)

↓

Resolve(Repository)

↓

Resolve(Logger)

↓

Construct Service
```

---

# Singleton Resolution

If the scope is `SINGLETON`

```
Resolve

↓

Singleton Cache

↓

Exists?

├── Yes → Return Existing Instance
└── No  → Construct → Cache → Return
```

Only one instance exists for the kernel lifetime.

---

# Request Resolution

If the scope is `REQUEST`

```
Resolve

↓

Request Cache

↓

Exists?

├── Yes → Return Existing Instance
└── No  → Construct → Cache → Return
```

The instance lives only for the active request.

---

# Transient Resolution

Transient objects are never cached.

```
Resolve

↓

Construct

↓

Return
```

Every resolution creates a new object.

---

# Circular Dependency Detection

During recursive resolution the validator maintains a dependency stack.

Example

```
A

↓

B

↓

C

↓

A
```

Results in

```
DependencyError

Circular dependency detected.
```

Construction stops immediately.

---

# Request Completion

At the end of request processing:

```python
container.end_request()
```

The request cache is destroyed.

```
Request Cache

↓

Disposed
```

Singletons remain alive.

---

# Kernel Shutdown

When the kernel stops:

```
Stop

↓

Dispose Singletons

↓

Clear Registry

↓

Shutdown Complete
```

Components implementing lifecycle hooks are shut down in reverse dependency order.

---

# Error Flow

```
Register

↓

Validate

↓

Resolve

↓

Construct

↓

Execute

↓

Success
```

Any failure produces one of the following:

- ValidationError
- DependencyError
- LifecycleError
- ComponentNotFoundError

Errors are propagated to the kernel for centralized handling.

---

# Thread Safety

The container guarantees:

- thread-safe singleton initialization
- isolated request scope
- immutable registrations after boot
- deterministic dependency resolution
- lock-free transient creation

---

# Performance Characteristics

| Operation | Complexity |
|-----------|-----------:|
| Register | O(1) |
| Registry Lookup | O(1) |
| Singleton Cache Lookup | O(1) |
| Request Cache Lookup | O(1) |
| Dependency Graph Validation | O(V + E) |
| Constructor Resolution | O(n) |

Where:

- **V** = registered components
- **E** = dependency relationships
- **n** = constructor dependency depth

---

# Execution Guarantees

The Container guarantees:

- deterministic resolution order
- immutable registration graph
- constructor injection only
- consistent scope behaviour
- automatic request cleanup
- lifecycle-aware component management
- thread-safe singleton creation
- complete dependency validation before execution

---

# Related Documentation

- README.md
- ARCHITECTURE.md
- DESIGN.md
- API.md

---

**Execution Model**

Deterministic • Immutable • Thread-Safe • Lifecycle-Aware
