# CAMEAL Kernel – Architectural Principles

These principles define the boundary of the kernel and must be preserved.

## 1. No Domain Logic

The kernel contains **no business logic**, **no domain intelligence**, and **no application-specific rules**.

- No RAG logic
- No ML models
- No reasoning rules
- No governance policies
- No document extraction rules
- No domain workflows

Those belong in engines and plugins that **consume** the kernel.

## 2. Infrastructure Only

The kernel provides **runtime infrastructure**:
- Lifecycle management
- Dependency injection
- Event bus
- Execution context
- Runtime managers
- Provider abstraction
- Orchestration
- Plugin framework

It does not provide domain capabilities.

## 3. Providers Expose Capabilities

Providers are infrastructure adapters.

They expose **standardized capabilities** (LLM, storage, vector, embedding, auth, etc.) to engines.

Providers contain **no intelligence**.

## 4. Engines Consume Providers

Engines (RAG, ML, Reasoning, etc.) are domain components.

They **consume** providers via the `ProviderRegistry`.

They should never instantiate infrastructure directly.

## 5. Communication is Event-Driven

Components communicate via the `EventBus`.

Events are immutable and carry only data, not behaviour.

## 6. Lifecycle is Centralised

All components implement the standard lifecycle:

`CREATED → INITIALIZED → STARTED → RUNNING → STOPPING → STOPPED`

The kernel coordinates component lifecycle during bootstrap and shutdown.

## 7. Services Interact Through Contracts

Components depend on **interfaces** (abstract base classes), not concrete implementations.

This enables:
- Loose coupling
- Testability
- Replaceability

## 8. Kernel is Versioned

All public APIs follow **Semantic Versioning**.

Breaking changes require a major version bump.

Internal implementation details may change without notice.

## 9. Kernel is Thread‑Safe

All components are thread‑safe.

Each request owns its own `ExecutionContext` and does not share mutable state.

## 10. Kernel is Observable

Every component emits lifecycle events, health checks, and metrics via `TelemetryProvider`.

Observability is built in, not bolted on.
