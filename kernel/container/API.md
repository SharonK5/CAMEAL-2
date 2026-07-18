# CAMEAL Kernel Container API

## Overview

The CAMEAL Kernel Container provides the dependency injection infrastructure for the CAMEAL runtime.

Its responsibilities are to:

- Register dependencies.
- Resolve dependencies.
- Manage object lifetimes.
- Perform constructor injection.
- Detect invalid dependency graphs.
- Support request-scoped execution.
- Provide a stable public API for kernel extensions.

The container is intentionally lightweight, deterministic, and thread-safe.

---

# API Stability

The CAMEAL Container distinguishes between **Public APIs**, **Extension APIs**, and **Internal APIs**.

Only the Public API is guaranteed to remain stable under Semantic Versioning.

---

## Stability Levels

| Level | Audience | Compatibility |
|---------|----------|---------------|
| Public API | Applications, plugins, engines | Stable |
| Extension API | Official CAMEAL modules | Stable with deprecation policy |
| Internal API | Kernel implementation | No compatibility guarantees |

---

# Semantic Versioning

The public API follows Semantic Versioning.

```
MAJOR.MINOR.PATCH
```

Example

```
1.4.2
```

Meaning

| Version | Description |
|-----------|------------|
| MAJOR | Breaking API changes |
| MINOR | New backwards-compatible functionality |
| PATCH | Bug fixes and performance improvements |

---

# Public API

The following classes constitute the official Container API.

| Class | Description |
|---------|-------------|
| Container | Dependency injection container |
| Scope | Object lifetime enumeration |
| Dependency | Dependency definition |
| Registration | Registration metadata |

These classes are safe for external use.

Breaking changes require a MAJOR release.

---

# Extension API

The Extension API exists for official CAMEAL engines and repositories.

Examples

```
RegistrationBuilder
ContainerBuilder
ScopeFactory
```

Extension APIs are:

- documented
- versioned
- covered by deprecation policy

but may evolve faster than the Public API.

---

# Internal API

The following components are implementation details.

| Component | Responsibility |
|------------|----------------|
| Resolver | Dependency resolution |
| Injector | Constructor injection |
| Registry | Dependency storage |
| Cache | Lifetime management |
| Validator | Graph validation |
| CycleDetector | Circular dependency detection |

These components are **not part of the public contract**.

External code must never import them directly.

---

# Container Class

The Container is the primary entry point.

Example

```python
from cameal.kernel.container import Container

container = Container()
```

---

## register()

Registers a dependency.

```python
register(
    interface,
    implementation,
    scope=Scope.TRANSIENT
)
```

Parameters

| Parameter | Description |
|------------|-------------|
| interface | Abstract type |
| implementation | Concrete implementation |
| scope | Lifetime |

Example

```python
container.register(
    Repository,
    SqlRepository,
    Scope.SINGLETON,
)
```

---

## resolve()

Resolves a dependency.

```python
resolve(interface)
```

Returns

```
Implementation instance
```

Example

```python
repo = container.resolve(Repository)
```

---

## contains()

Returns whether a dependency exists.

```python
container.contains(Repository)
```

Returns

```
True
```

or

```
False
```

---

## unregister()

Removes a registration.

```python
container.unregister(Repository)
```

---

## clear()

Removes all registrations.

```python
container.clear()
```

---

# Scope

Supported lifetimes.

## SINGLETON

One instance for the lifetime of the kernel.

```
Kernel
 ├──── Repository
 ├──── Repository
 └──── Repository

Same instance
```

---

## REQUEST

One instance per request.

```
Request A

Repository A

Request B

Repository B
```

---

## TRANSIENT

Always creates a new object.

```
Resolve()

↓

New Instance

Resolve()

↓

New Instance
```

---

# Constructor Injection

Dependencies are resolved automatically from constructor signatures.

Example

```python
class UserService:

    def __init__(
        self,
        repository: Repository,
        logger: Logger,
    ):
        ...
```

The container resolves both dependencies automatically.

---

# Request Scope

During request execution

```python
container.begin_request()

...

container.end_request()
```

Request-scoped objects are automatically released.

---

# Exceptions

The public API raises the following exceptions.

| Exception | Description |
|------------|-------------|
| DependencyError | Resolution failure |
| ValidationError | Invalid registration |
| LifecycleError | Invalid lifecycle transition |
| ComponentNotFoundError | Unknown dependency |

---

# Thread Safety

The container guarantees:

- thread-safe singleton creation
- request isolation
- immutable registrations after bootstrap
- deterministic resolution

---

# Dependency Graph Validation

Before startup the container validates:

- missing dependencies
- duplicate registrations
- circular dependencies
- invalid scopes

Failure prevents kernel startup.

---

# Compatibility Rules

## PATCH

Allowed

- documentation
- bug fixes
- optimizations

Forbidden

- API changes

---

## MINOR

Allowed

- new methods
- new scopes
- new overloads
- optional parameters

Forbidden

- signature changes
- removed methods

---

## MAJOR

Allowed

- redesign
- interface changes
- removals

Requires

- migration guide
- compatibility notes
- changelog

---

# Deprecation Policy

Public APIs follow a staged removal process.

```
Stable
    │
    ▼
Deprecated
    │
    ▼
Runtime Warning
    │
    ▼
Migration Guide
    │
    ▼
Removed in Next Major Version
```

Deprecated APIs remain functional until the next MAJOR release.

---

# Plugin Compatibility

Plugins declare compatible kernel versions.

Example

```yaml
kernel:
  min_version: "1.0.0"
  max_version: "2.0.0"
```

Bootstrap validates compatibility before plugin activation.

---

# Runtime Guarantees

The Container guarantees:

- deterministic dependency resolution
- constructor injection
- immutable registration graph after bootstrap
- request isolation
- singleton consistency
- thread safety
- circular dependency detection
- lifecycle consistency

---

# Example

```python
from cameal.kernel.container import (
    Container,
    Scope,
)

container = Container()

container.register(
    Repository,
    SqlRepository,
    Scope.SINGLETON,
)

container.register(
    UserService,
    UserService,
    Scope.TRANSIENT,
)

service = container.resolve(UserService)

service.execute()
```

---

# Related Documentation

- README.md
- ARCHITECTURE.md
- DESIGN.md
- EXECUTION_FLOW.md

---

**API Version**

```
1.0.0
```

**Status**

**Stable Public API**
