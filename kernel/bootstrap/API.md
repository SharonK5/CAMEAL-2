# Bootstrap API

**Package:** `cameal.kernel.bootstrap`

**Version:** 1.0.0

**API Status:** Stable

---

# Overview

The Bootstrap subsystem is responsible for constructing a valid CAMEAL Kernel runtime.

It assembles all runtime infrastructure, validates configuration and dependencies, discovers plugins, registers components, freezes the dependency container, and returns a fully initialized `Kernel` instance.

Bootstrap performs **construction only**.

It never executes requests, performs orchestration, or contains business logic.

---

# Public API

The Bootstrap subsystem exposes a deliberately small public API.

| Class | Purpose | Stability |
|---------|----------|-----------|
| Bootstrap | Entry point for building the runtime | Stable |
| Builder | Constructs the Kernel instance | Stable |
| Configuration | Loads and validates configuration | Stable |

Everything else should be considered internal implementation details.

---

# Bootstrap

## Description

Primary entry point for creating a CAMEAL runtime.

Normally applications interact only with this class.

---

## Methods

### bootstrap()

```python
Bootstrap.bootstrap(config) -> Kernel
```

Builds and returns a fully initialized kernel.

### Parameters

| Name | Type | Description |
|------|------|-------------|
| config | Configuration \| dict \| Path | Runtime configuration |

### Returns

```python
Kernel
```

### Raises

- ConfigurationError
- ValidationError
- DependencyError
- PluginError

---

## Example

```python
from cameal.kernel.bootstrap import Bootstrap

kernel = Bootstrap.bootstrap(config)
```

---

# Builder

## Description

Responsible for assembling the runtime components into a Kernel instance.

Builder coordinates:

- Dependency Container
- Managers
- Plugin Discovery
- Repository Registration
- Engine Registration
- Workflow Registration

---

## Methods

### build()

```python
Builder.build() -> Kernel
```

Constructs a complete runtime.

---

# Configuration

## Description

Loads runtime configuration from supported sources.

Supported sources include:

- YAML
- JSON
- Environment Variables
- Python Objects

---

## Methods

### load()

```python
Configuration.load(source)
```

Loads configuration.

---

### validate()

```python
Configuration.validate()
```

Validates configuration values.

---

# Runtime Construction Sequence

The Bootstrap subsystem follows a deterministic construction sequence.

```text
Load Configuration
        │
        ▼
Validate Configuration
        │
        ▼
Discover Plugins
        │
        ▼
Load Manifests
        │
        ▼
Validate Dependencies
        │
        ▼
Create Container
        │
        ▼
Register Managers
        │
        ▼
Register Repositories
        │
        ▼
Register Engines
        │
        ▼
Register Providers
        │
        ▼
Register Workflows
        │
        ▼
Freeze Container
        │
        ▼
Validate Runtime
        │
        ▼
Build Kernel
        │
        ▼
Return Kernel
```

---

# Error Model

Bootstrap may raise the following exceptions.

| Exception | Description |
|------------|-------------|
| ConfigurationError | Invalid runtime configuration |
| ValidationError | Runtime validation failed |
| DependencyError | Dependency graph is invalid |
| PluginError | Plugin discovery or loading failed |

---

# Thread Safety

Bootstrap is intended to execute once during application startup.

After construction, the returned Kernel is responsible for runtime execution.

Bootstrap itself is **not** intended for concurrent runtime use.

---

# Stability

## Stable Public API

- Bootstrap
- Builder
- Configuration

These classes follow semantic versioning.

Minor releases will remain backward compatible.

---

## Internal API (Unstable)

The following classes are internal implementation details and may change without notice.

- Discovery
- Registrar
- Loader
- Validator
- Initializer
- DependencyGraph

Applications should never depend on these classes directly.

---

# Versioning

Bootstrap follows Semantic Versioning.

| API | Version |
|------|---------|
| Package | 1.0.0 |
| Public API | 1.0 |
| Status | Stable |

---

# Design Principles

The Bootstrap subsystem guarantees:

- Deterministic runtime construction
- Dependency validation before startup
- Immutable runtime configuration after initialization
- Plugin discovery without kernel modification
- Separation of construction from execution
- Consistent runtime initialization across deployments

Bootstrap constructs the runtime.

The Kernel executes the runtime.
