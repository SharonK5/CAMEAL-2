# CAMEAL Kernel Container – Design

## Purpose

The Container implements dependency injection for the CAMEAL Kernel.

Its purpose is to construct runtime objects, resolve dependencies,
manage object lifetimes, and isolate components from concrete
implementations.

The design follows SOLID principles and emphasizes deterministic,
testable, and thread-safe object composition.

---

# Design Objectives

The container is designed to provide:

- Constructor-based dependency injection
- Type-safe dependency resolution
- Loose coupling
- Lifetime management
- Thread safety
- High testability
- Low runtime overhead
- Extensibility

---

# Design Principles

## Single Responsibility Principle

Each class has one responsibility.

| Component | Responsibility |
|-----------|----------------|
| Container | Public dependency API |
| Registration | Represents a registration |
| Registry | Stores registrations |
| Resolver | Resolves dependency graphs |
| Injector | Creates objects |
| Validator | Validates dependency graphs |
| Cache | Manages runtime instances |
| Scope | Defines object lifetime |

---

## Open / Closed Principle

The container is open for extension.

New scopes, validation rules, caching strategies,
or construction mechanisms can be added without
modifying existing components.

---

## Liskov Substitution

All implementations must satisfy the same contracts.

Resolvers, caches, registries, and injectors may be replaced
without affecting the kernel.

---

## Interface Segregation

Each component exposes only the methods required
for its responsibility.

No component depends upon unnecessary interfaces.

---

## Dependency Inversion

All runtime components depend upon abstractions.

Concrete implementations are registered during bootstrap.

---

# Design Patterns

## Dependency Injection

The primary pattern.

```
Client

↓

Container

↓

Resolver

↓

Injector

↓

Instance
```

---

## Registry Pattern

All registrations are stored centrally.

```
Interface

↓

Registration

↓

Registry
```

---

## Factory Pattern

The injector behaves as a runtime object factory.

```
Constructor

↓

Resolve Parameters

↓

Create Instance
```

---

## Strategy Pattern

Scopes represent interchangeable lifetime strategies.

```
Singleton

Request

Transient
```

---

## Composition Root

The Bootstrap component is the composition root.

Only Bootstrap registers dependencies.

Engines never register themselves.

---

# Lifetime Design

## Singleton

Created once.

Shared for the lifetime of the kernel.

Examples

- EventBus
- Configuration
- RepositoryManager

---

## Request

Created once per request.

Disposed after request completion.

Examples

- ExecutionContext
- ReasoningSession

---

## Transient

Created every resolution.

Never cached.

Examples

- Validators
- Builders
- DTO Mappers

---

# Constructor Injection

Only constructor injection is supported.

```
class ReasoningEngine:

    def __init__(
        self,
        repository: Repository,
        policy: PolicyEngine,
    ):
        ...
```

Field injection and property injection are intentionally prohibited.

---

# Registration Model

Every registration contains:

- Interface
- Implementation
- Lifetime Scope
- Optional Factory
- Optional Metadata

Example

```
Repository
        │
        ▼
SQLRepository
        │
        ▼
Singleton
```

---

# Resolution Algorithm

```
Resolve()

↓

Lookup Registration

↓

Validate

↓

Cache Lookup

↓

Resolve Constructor Parameters

↓

Construct Instance

↓

Cache (optional)

↓

Return Instance
```

Resolution is recursive.

Each dependency is resolved independently.

---

# Validation Rules

The Validator checks:

- duplicate registrations
- missing registrations
- circular dependencies
- constructor compatibility
- invalid scope configuration

Validation occurs before object construction.

---

# Caching Strategy

Only Singleton and Request scopes are cached.

```
Singleton Cache

Repository

EventBus

Configuration

──────────────

Request Cache

ExecutionContext

WorkflowContext
```

Transient instances are never cached.

---

# Thread Safety

The implementation guarantees:

- thread-safe singleton creation
- isolated request caches
- immutable registrations
- lock-free transient construction

---

# Error Handling

Failures produce strongly typed exceptions.

Examples

- RegistrationError
- ResolutionError
- CircularDependencyError
- ScopeError

The container never returns partially constructed objects.

---

# Design Constraints

The Container SHALL NOT

- execute workflows
- invoke engines
- evaluate policies
- perform reasoning
- access repositories
- publish events
- implement business logic

Its responsibility ends once an object has been created.

---

# Performance Considerations

The implementation is optimized for:

- O(1) registration lookup
- lazy object construction
- minimal allocations
- singleton reuse
- request-local caching

---

# Testability

The design supports:

- dependency substitution
- mock injection
- deterministic construction
- isolated unit testing
- constructor verification

Every component can be tested independently.

---

# Future Extensions

The design supports future additions such as:

- named registrations
- conditional bindings
- generic type resolution
- child containers
- module-based registration
- distributed dependency providers

without breaking existing APIs.
