kernel/providers/ARCHITECTURE.md` (Updated to match refined README)

```markdown
# Providers Architecture

## Overview

Providers are infrastructure adapters that bridge the CAMEAL Kernel Runtime with external technologies and services. They expose standardized capabilities (LLM, storage, vector search, etc.) while containing **no business decision logic**.

## Architectural Principles

1. **Contract over Implementation** – The kernel depends on provider interfaces, not concrete implementations.

2. **Capability Boundaries** – Each provider category represents an independent capability (storage, vector, LLM, etc.).

3. **Lifecycle Integration** – Providers are first-class runtime citizens with start/stop/health management.

4. **Engine Independence** – Engines consume provider capabilities through the registry, never directly instantiating providers.

5. **Infrastructure Isolation** – External dependencies are contained within provider implementations, keeping the kernel core clean.

## High-Level Architecture
┌─────────────────────────────────────────────────────────────────┐
│ Kernel Runtime │
│ │
│ ┌───────────┐ ┌───────────┐ ┌───────────────────────┐ │
│ │ Engine │ │ Engine │ │ Intelligence Layer │ │
│ │ (RAG) │ │ (ML) │ │ (Reasoning, etc.) │ │
│ └─────┬─────┘ └─────┬─────┘ └───────────┬───────────┘ │
│ │ │ │ │
│ └────────────────┼───────────────────────┘ │
│ │ │
│ ┌──────▼──────┐ │
│ │ Provider │ │
│ │ Registry │ │
│ └──────┬──────┘ │
│ │ │
│ ┌────────────────┼───────────────────────────────┐ │
│ │ │ │ │
│ ┌─────▼─────┐ ┌─────▼─────┐ ┌──────────────────┴──┐ │
│ │ Storage │ │ LLM │ │ Vector Store │ │
│ │ Provider │ │ Provider │ │ Provider │ │
│ └───────────┘ └───────────┘ └─────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────┘

text
Copy
Download

## Components

### Provider (base/provider.py)
Abstract base class that all providers implement. Extends `Lifecycle` for start/stop/health management.

**Key Method:**
- `get()` – Returns the underlying client or resource.

### ProviderRegistry (registry/provider_registry.py)
Thread-safe registry that stores providers by unique name.

**Key Methods:**
- `register(name, provider)` – Registers a provider.
- `get(name)` – Resolves a provider by name.
- `has(name)` – Checks if a provider exists.
- `list()` – Lists all registered provider names.

### ProviderLifecycle (lifecycle/provider_lifecycle.py)
Manages lifecycle operations across all providers.

**Key Methods:**
- `start_all()` – Starts all providers.
- `stop_all()` – Stops all providers.
- `health_all()` – Checks health of all providers.

## Provider Categories

Each category is a capability boundary with its own interface:

| Category | Purpose | Examples |
|----------|---------|----------|
| **storage/** | Object/file storage | S3, filesystem, database |
| **vector/** | Vector search | FAISS, Pinecone, Qdrant |
| **embedding/** | Embedding generation | SentenceTransformers, OpenAI |
| **llm/** | Language models | Ollama, OpenAI, Anthropic |
| **data/** | External data | APIs, databases |
| **model/** | ML models | ONNX, PyTorch |
| **authentication/** | Identity & access | OAuth2, JWT |
| **telemetry/** | Observability | Prometheus, OpenTelemetry |

## Relationship with Engines

**Providers** – infrastructure adapters (LLM clients, storage, vector stores)

↓ consume

**Engines** – intelligence layer (RAG, ML, Reasoning, Analytics, Drafting)

Engines contain business logic and decision-making. Providers contain only infrastructure interaction.

## Lifecycle Flow
Bootstrap
│
├── Create providers
│
├── Register with ProviderRegistry
│
├── ProviderLifecycle.start_all()
│
▼
Running State
│
├── Engines resolve providers via registry
│
├── Engines call provider.get() for clients
│
▼
Shutdown
│
└── ProviderLifecycle.stop_all()

text
Copy
Download

## Thread Safety

- `ProviderRegistry` uses `RLock` for thread-safe registration and resolution.
- Providers should be designed thread-safe if accessed concurrently.

## Error Handling

| Scenario | Response |
|----------|----------|
| Provider not found | `ProviderNotFoundError` |
| Duplicate registration | `ProviderRegistrationError` |
| Provider start fails | Kernel start may fail (configurable) |
| Provider unhealthy | Health monitor reports, engines can retry |

## Extensibility

New provider types are added by:
1. Creating a new subdirectory (e.g., `cache/`)
2. Defining a new abstract class extending `Provider`
3. Implementing concrete providers
4. No changes needed to registry or lifecycle

## Security

- Providers should not expose credentials in `get()` output.
- Use the `SecretsProvider` for managing sensitive configuration.
- Follow the principle of least privilege.

## Testing

- **Unit tests** – Registry, lifecycle, and individual provider tests.
- **Contract tests** – Verify all providers implement the interface correctly.
- **Integration tests** – Validate with real external services (optional, isolated).
