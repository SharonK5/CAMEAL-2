# CAMEAL Kernel Diagnostics

## Overview

The Diagnostics subsystem provides runtime observability for the CAMEAL Kernel. It integrates with the kernel's lifecycle, events, and telemetry infrastructure to deliver:

- **Health checks** – aggregate health status of all components
- **Metrics** – runtime metrics (counters, gauges, histograms)
- **Tracing** – distributed tracing via spans and events
- **Logging** – structured logging with correlation

Diagnostics is a **kernel‑internal** subsystem. It provides the foundation for monitoring, but does not contain domain‑specific monitoring logic.

## Why It Exists

Without diagnostics, the kernel is a black box. Operators cannot:

- Know if all components are healthy.
- Monitor performance trends.
- Trace execution paths through workflows and plugins.
- Correlate logs across requests.

Diagnostics brings observability into the kernel's managed runtime, providing:

- **Centralised health** – one view of all component statuses.
- **Performance insights** – metrics for workflows, jobs, and providers.
- **Traceability** – end‑to‑end trace from scheduler to provider.
- **Structured logging** – logs with request/trace IDs for filtering.

## Responsibilities

The diagnostics subsystem is responsible for:

- **Aggregating health** – querying all `Lifecycle` components for their health status.
- **Collecting metrics** – capturing runtime metrics from components and providers.
- **Tracing execution** – building trace trees from events emitted by workflows, jobs, and orchestrator.
- **Structured logging** – consuming log events and enriching them with correlation IDs.

The diagnostics subsystem does **not**:

- Define domain‑specific monitoring rules (e.g., "CPU > 80%").
- Store historical data (traces and logs are held in‑memory with a configurable limit).
- Perform alerting – that is left to higher‑level monitoring systems.

## Architecture

Diagnostics is built around the `EventBus`:
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Scheduler │──────▶│ │ │ │
├─────────────┤ │ │ │ Health │
│ Workflow │──────▶│ EventBus │──────▶│ Checks │
├─────────────┤ │ │ │ │
│ Orchestrator│──────▶│ │ │ Metrics │
├─────────────┤ └─────────────┘ │ │
│ Plugin │────────────────────────────▶ Tracing │
├─────────────┤ │ │
│ Provider │────────────────────────────▶ Logging │
└─────────────┘ └─────────────┘

text
Copy
Download

All diagnostics data is collected from events and component health methods, without any additional instrumentation.

## Components

- **HealthChecker** – aggregates health status from all `Lifecycle` components.
- **MetricsCollector** – collects runtime metrics (queue lengths, throughput, etc.) and emits them via `TelemetryProvider`.
- **Tracer** – subscribes to events and builds trace trees (spans with parent‑child relationships).
- **Logger** – subscribes to log events and enriches them with correlation IDs (trace_id, span_id, request_id).

## Integration with Other Subsystems

| Subsystem      | Role                                                          |
|----------------|---------------------------------------------------------------|
| **Lifecycle**  | Provides health status for all components.                    |
| **Events**     | All diagnostics data flows through the EventBus.              |
| **TelemetryProvider** | Emits metrics and logs externally.                     |
| **Orchestrator** | Traces workflow execution.                                   |
| **Scheduler**  | Traces job execution.                                         |

## Examples

### Get health status

```python
from kernel.diagnostics import Diagnostics

diagnostics = Diagnostics(event_bus, telemetry_provider)
health = diagnostics.health()
print(health)
# {'scheduler': 'healthy', 'workflows': 'healthy', 'plugins': 'healthy'}
View recent traces
python
Copy
Download
traces = diagnostics.traces(limit=5)
for trace in traces:
    print(f"{trace['type']} {trace['workflow']} completed in {trace['duration']}ms")
Get metrics snapshot
python
Copy
Download
metrics = diagnostics.metrics()
print(metrics)
# {'timestamp': 1712345678.0, 'workflows_run': 42, 'jobs_completed': 10}
Documentation
ARCHITECTURE.md – System architecture

DESIGN.md – Design decisions and principles

API.md – Public API reference
