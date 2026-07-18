# CAMEAL Kernel Lifecycle – Design

## Purpose

The Lifecycle subsystem provides a standardised execution contract for all kernel-managed components. Its design ensures that every component—regardless of its internal complexity—can be started, stopped, and monitored in a predictable, repeatable, and observable manner.

This document explains the design decisions, patterns, trade-offs, and rationale behind the Lifecycle subsystem.

---

## Design Objectives

The Lifecycle subsystem is designed to achieve:

- **Uniformity** – Every component follows the same lifecycle, reducing cognitive load.
- **Predictability** – Startup and shutdown order are deterministic.
- **Observability** – All transitions are logged and emit events.
- **Resilience** – Failures are isolated and reported.
- **Simplicity** – The interface is minimal and intuitive.

---

## Design Principles

1. **Separation of Concerns** – Lifecycle management is separate from business logic. Components implement lifecycle methods; the LifecycleManager coordinates them.

2. **Explicit Transitions** – Each transition is a distinct method (e.g., `initialize()`, `start()`). This makes the lifecycle self‑documenting.

3. **Validation** – All transitions are validated against a state machine. Invalid transitions raise `LifecycleError`.

4. **Idempotency** – Lifecycle operations are idempotent where possible (e.g., `stop()` can be called multiple times safely).

5. **Observability** – Every transition emits an event for monitoring, audit, and diagnostics.

6. **Graceful Degradation** – Failures are logged and published; the manager continues with remaining components.

---

## Design Patterns

| Pattern | Usage |
|---------|-------|
| **Template Method** | `Lifecycle` defines the skeleton of the lifecycle; subclasses implement `_on_health()` and optionally override other hooks. |
| **State Pattern** | `LifecycleState` represents the current state; transitions are validated via a transition table. |
| **Observer** | `LifecycleObserver` receives lifecycle events, enabling decoupled monitoring and logging. |
| **Mediator** | `LifecycleManager` mediates between the kernel and all lifecycle components. |
| **Strategy** | Health reporting is a strategy; different components may implement different health logic. |

---

## Design Decisions

### 1. Separate State from Health

**Decision**: State and health are independent.

**Rationale**: A component may be running (`RUNNING`) but degraded (e.g., a repository with a failing connection). Treating them separately allows finer-grained monitoring.

### 2. Optional Pause/Resume

**Decision**: `pause()` and `resume()` are not part of the base `Lifecycle` interface. Instead, they are defined in an optional `Pausable` protocol.

**Rationale**: Not all components can meaningfully pause (e.g., a registry, a container). Forcing them to implement no-op methods violates Interface Segregation Principle.

### 3. Terminal FAILED State

**Decision**: `FAILED` is a terminal state reachable from any other state.

**Rationale**: Failures can occur at any phase. Having a single terminal state simplifies error handling and recovery.

### 4. Idempotent Lifecycle Operations

**Decision**: Operations like `stop()` are idempotent; calling them multiple times has no additional effect.

**Rationale**: In distributed or error‑prone environments, components may receive duplicate signals. Idempotency ensures safety.

### 5. Deterministic Ordering

**Decision**: Components are started in registration order and stopped in reverse order.

**Rationale**: This prevents orphaned dependencies and ensures that resources are released in the correct sequence.

### 6. Lifecycle Events

**Decision**: Every state transition emits a lifecycle event.

**Rationale**: This enables observability without tight coupling. Monitoring, audit, and diagnostics can subscribe without modifying the component.

---

## Design Trade‑offs

| Trade‑off | Choice | Rationale |
|-----------|--------|-----------|
| **Synchronous vs Asynchronous** | Synchronous lifecycle methods | Simpler to reason about; easier to test; can be made async later if needed. |
| **Global vs Per‑component State** | Per‑component state | Each component owns its own state; the manager only orchestrates. |
| **Strict vs Loose Validation** | Strict validation | Invalid transitions are caught early, preventing undefined behaviour. |
| **Pause/Resume in Base Interface** | Excluded from base; optional | Keeps the base contract minimal; components that support pause can opt in. |

---

## Implementation Rationale

### Why Abstract Base Class?

Using `ABC` ensures that all components implement `_on_health()`. Default implementations for other methods reduce boilerplate while allowing overrides.

### Why Enums for States and Health?

Enums provide type safety, prevent typos, and make state transitions explicit.

### Why Separate Transition Table?

The transition table (`transitions.py`) centralises validation logic, making it easy to review and extend.

### Why Observers?

Observers decouple event handling from lifecycle logic. The same component can be observed by monitoring, logging, and auditing subsystems without modification.

---

## Error Handling Strategy

- **Invalid transitions** → `LifecycleError` (immediate failure).
- **Component failures** → Component transitions to `FAILED`; other components continue.
- **Aggregate failures** → The manager logs and reports; recovery is delegated to higher‑level orchestration.

---

## Threading Model

- State transitions are **not** thread‑safe; they are intended to be called from a single orchestrator (the `LifecycleManager`).
- Health checks **are** thread‑safe; they should not modify state.
- The `LifecycleManager` uses a lock to serialise transitions across components.

---

## Testability

The design supports:

- **Unit testing** – Each component can be tested in isolation.
- **Integration testing** – The manager can be tested with multiple components.
- **Mocking** – Lifecycle methods can be mocked for dependency testing.
- **State validation** – Transition tables are independently testable.

---

## Future Proofing

The current design supports future enhancements without breaking the contract:

- **Rolling restart** – Components can be restarted individually.
- **Hot plugin reload** – New components can be registered and started dynamically.
- **Distributed lifecycle** – The manager could be extended to coordinate across multiple processes.
- **Remote health probes** – Health reports can be exposed via an API.

---

## Related Documentation

- [README.md](README.md) – Overview and usage.
- [ARCHITECTURE.md](ARCHITECTURE.md) – Internal architecture and component relationships.
- [API.md](API.md) – Public interfaces and contracts.
- [EXECUTION_FLOW.md](EXECUTION_FLOW.md) – State transition and execution flow.
