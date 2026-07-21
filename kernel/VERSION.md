# CAMEAL Kernel Runtime – Version

**Current Version:** 1.0.0  
**Status:** Stable / Production‑Ready  
**Release Date:** 2026‑07‑21  

The CAMEAL Kernel Runtime is a modular, event‑driven, dependency‑injected orchestration platform designed to host intelligence engines, workflows, and plugins.

---

## Versioning Policy

The kernel follows **Semantic Versioning (SemVer)**:

- **MAJOR** version (`X.0.0`) – Incompatible public API changes.
- **MINOR** version (`0.X.0`) – Backward‑compatible new functionality.
- **PATCH** version (`0.0.X`) – Backward‑compatible bug fixes.

All public APIs are versioned. Internal implementation details may change without notice.

---

## Public API (Stable)

The following components are considered **public API** and are subject to SemVer:

- `kernel.Kernel`
- `kernel.lifecycle.Lifecycle`
- `kernel.container.Container`
- `kernel.events.EventBus` and `kernel.events.Event`
- `kernel.context.ExecutionContext`
- `kernel.managers.*` (all manager classes)
- `kernel.bootstrap.Bootstrap`
- `kernel.orchestrator.Orchestrator`
- `kernel.providers.Provider` and `kernel.providers.ProviderRegistry`
- `kernel.plugins.Plugin`
- `kernel.workflows.Workflow`
- `kernel.scheduler.Scheduler`
- `kernel.diagnostics.Diagnostics`

---

## Internal API (Unstable)

The following are **internal implementation details** and may change in any release:

- `kernel.bootstrap.builder`
- `kernel.bootstrap.registrar`
- `kernel.bootstrap.discovery`
- `kernel.bootstrap.loader`
- `kernel.bootstrap.validator`
- `kernel.bootstrap.initializer`
- `kernel.container.registry`
- `kernel.events.dispatcher`
- `kernel.managers.registry`
- `kernel.orchestrator.router`
- `kernel.orchestrator.planner`
- `kernel.orchestrator.executor`
- `kernel.orchestrator.dispatcher`
- `kernel.orchestrator.validator`
- `kernel.providers.*.implementations` (unless specifically documented)

---

## Quality Gates for v1.0.0

- ✅ ~250 tests passing
- ✅ 0 failures
- ✅ 0 errors
- ✅ All subsystems stable and tested
- ✅ Documentation complete (API, Architecture, Extension Guide, Principles)

---

## Compatibility Statement

- **Backward‑compatible enhancements** are allowed in MINOR and PATCH releases.
- **Breaking changes** require a MAJOR version bump.
- Deprecated features will be marked with `@deprecated` and remain for one full minor release.
- Plugins must declare kernel compatibility in their `manifest.yaml`.

---

## Roadmap

- **v1.1.0** – Additional plugin types, enhanced observability, optional persistence.
- **v2.0.0** – Future extensions may introduce breaking changes (if required).

---

**For detailed release notes, see [CHANGELOG.md](CHANGELOG.md).**
