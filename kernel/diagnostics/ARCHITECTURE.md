## 📄 `kernel/diagnostics/ARCHITECTURE.md`

```markdown
# Diagnostics Architecture

## High‑Level Design
┌─────────────────────────────────────────────────────────────┐
│ Diagnostics │
│ │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ DiagnosticsRegistry │ │
│ │ (stores health checks, metric providers, │ │
│ │ trace providers, log providers) │ │
│ └───────────────────────────┬───────────────────────────┘ │
│ │ │
│ ┌───────────────────────────▼───────────────────────────┐ │
│ │ Diagnostics │ │
│ │ (unified interface for health, metrics, tracing, │ │
│ │ logging) │ │
│ └───────────────────────────┬───────────────────────────┘ │
│ │ │
│ ┌───────────────────────┼───────────────────────┐ │
│ │ │ │ │
│ ┌───▼───────────┐ ┌────────▼──────────┐ ┌───────▼─────┐│
│ │ Health │ │ Metrics │ │ Tracer ││
│ │ Checker │ │ Collector │ │ ││
│ └───────────────┘ └────────────────────┘ └─────────────┘│
│ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Logger │ │
│ └─────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Event Bus │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

text
Copy
Download

## Components

### 1. Diagnostics Registry

A thread‑safe registry that allows components to register:

- **Health checks** – functions that return `HealthStatus`
- **Metric providers** – functions that return metric snapshots
- **Trace providers** – functions that return trace data
- **Log providers** – functions that return log entries

By default, diagnostics uses the EventBus to collect data, but registry providers can override or augment this.

### 2. Health Checker

- Aggregates health status from all registered health checks.
- Also queries known `Lifecycle` components (managers, orchestrator, scheduler) if they are not explicitly registered.
- Returns a dictionary of component name → HealthStatus.

### 3. Metrics Collector

- Collects runtime metrics from registered metric providers.
- Typical metrics: component status, event counts, queue sizes, execution times.
- Emits metrics via the `TelemetryProvider` if configured.

### 4. Tracer

- Subscribes to the EventBus for events.
- Builds trace trees: each trace has a root span (e.g., a job start) and child spans (e.g., workflow steps).
- Traces are stored in‑memory with a configurable limit.

### 5. Logger

- Subscribes to the EventBus for log events.
- Enriches logs with correlation IDs (trace_id, span_id, request_id) extracted from the event metadata.
- Stores logs in‑memory with a configurable limit.

## Data Flow

1. Components emit events to the EventBus.
2. The Tracer and Logger subscribe to the EventBus.
3. The Tracer builds and stores trace trees.
4. The Logger stores enriched log entries.
5. On demand, the Diagnostics API returns health, metrics, traces, and logs.
6. If a TelemetryProvider is configured, metrics and logs are also emitted externally.

## Thread Safety

- The DiagnosticsRegistry uses `RLock` for thread‑safe registration and access.
- The Diagnostics class is designed to be used from a single thread (the main loop), but its methods are safe for concurrent access.

## Dependencies

- `kernel.events` – for subscribing to events.
- `kernel.providers.telemetry` – for emitting metrics and logs.
- `kernel.lifecycle` – for health status definitions.

Diagnostics does not depend on other kernel subsystems (scheduler, workflows, etc.) except through the EventBus.
