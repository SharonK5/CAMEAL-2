# CAMEAL Kernel Runtime – Changelog

All notable changes to the CAMEAL Kernel Runtime are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] – 2026-07-21

### Added – Foundation Release

The first stable release of the CAMEAL Kernel Runtime.

#### Core Subsystems

- **Lifecycle** – standardised start/stop/health for all components.
- **Container** – dependency injection with singleton and request scopes.
- **Events** – publish/subscribe with validation, filtering, and execution pipelines.
- **Context** – immutable, request‑scoped execution context.
- **Managers** – runtime registries for engines, workflows, repositories, plugins, and schedulers.
- **Bootstrap** – assembles the kernel from configuration and plugins.
- **Orchestrator** – coordinates workflow execution via planners, routers, dispatchers, and executors.
- **Providers** – infrastructure adapters (storage, LLM, vector, embedding, data, auth, telemetry).
- **Plugins** – discovery, loading, and registration of extensions.
- **Workflows** – declarative execution graphs (YAML/JSON).
- **Scheduler** – automated, time‑based execution of workflows.
- **Diagnostics** – health, metrics, tracing, and logging for the runtime.

#### Documentation

- `README.md` – overview and getting started.
- `ARCHITECTURE.md` – system architecture and component relationships.
- `DESIGN.md` – design decisions and principles.
- `API.md` – public API reference.
- `EXECUTION_FLOW.md` – end‑to‑end runtime flow.
- `EXTENSION_GUIDE.md` – how to extend the kernel.
- `KERNEL_PRINCIPLES.md` – architectural rules and boundaries.
- `VERSION.md` – versioning policy and quality gates.
- `CHANGELOG.md` – this file.
- `manifest.yaml` – subsystem metadata.

#### Quality Gates

- ~250 tests passing
- 0 failures
- 0 errors
- All subsystems stable and tested

#### Test Coverage

| Subsystem    | Tests | Status |
|--------------|-------|--------|
| Lifecycle    | ✓     | ✅     |
| Container    | 18    | ✅     |
| Events       | 26    | ✅     |
| Context      | 15    | ✅     |
| Managers     | 25    | ✅     |
| Bootstrap    | 34    | ✅     |
| Orchestrator | 26    | ✅     |
| Providers    | ~100  | ✅     |
| Plugins      | 12    | ✅     |
| Workflows    | 13    | ✅     |
| Scheduler    | 9     | ✅     |
| Diagnostics  | 24    | ✅     |
| **Total**    | **~250** | ✅     |

---

## [Unreleased]

### Planned for v1.1.0

- **Enhanced plugin types** – event‑based triggers, lifecycle hooks.
- **Observability extensions** – integration with OpenTelemetry, Prometheus export.
- **Optional persistence** – for job and workflow state.

---

## [0.1.0] – 2026-06-xx (Development Phase)

Initial development and prototyping. Subsystems built incrementally:

- Lifecycle
- Container
- Events
- Context
- Managers
- Bootstrap
- Orchestrator
- Providers
- Plugins
- Workflows
- Scheduler
- Diagnostics

All subsystems stabilised and tested as individual units before integration into v1.0.0.
