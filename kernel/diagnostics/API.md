# Diagnostics API Reference

## `Diagnostics`

```python
class Diagnostics:
    def __init__(
        self,
        event_bus: EventBus,
        telemetry_provider: Optional[TelemetryProvider] = None,
        registry: Optional[DiagnosticsRegistry] = None,
        trace_limit: int = 100,
    ):
        """
        Initialize diagnostics.

        Args:
            event_bus: The kernel's event bus.
            telemetry_provider: Optional provider for emitting metrics and logs.
            registry: Optional custom registry (defaults to a new instance).
            trace_limit: Maximum number of traces to keep in memory.
        """
Methods

start() -> None – Subscribe to events and begin collecting data.

stop() -> None – Unsubscribe and clean up.

health() -> Dict[str, HealthStatus] – Return health status of all registered components.

metrics() -> Dict[str, Any] – Return a snapshot of current metrics.

traces(limit: Optional[int] = None) -> List[Dict] – Return recent traces (last limit).

logs(limit: Optional[int] = None, level: Optional[str] = None) -> List[Dict] – Return recent logs, filtered by log level if provided.

DiagnosticsRegistry
python
Copy
Download
class DiagnosticsRegistry:
    def register_health_check(self, name: str, check: Callable[[], HealthStatus]) -> None
    def register_metric_provider(self, name: str, provider: Callable[[], Any]) -> None
    def register_trace_provider(self, name: str, provider: Callable[[], List[Dict]]) -> None
    def register_log_provider(self, name: str, provider: Callable[[], List[Dict]]) -> None
Use these methods to provide custom health checks, metrics, traces, and logs that are not automatically collected via the EventBus.

Events Consumed
Diagnostics subscribes to all events (using '*'). It recognises the following event types for special handling:

component.health – custom health check events.

workflow.started, workflow.completed – trace workflow execution.

job.started, job.completed – trace job execution.

log.debug, log.info, log.warn, log.error – structured log entries.

Other events are treated as generic events and stored as traces/logs depending on their content.

Telemetry Integration
If a TelemetryProvider is provided, Diagnostics will:

Emit a metric for each event received (count by type).

Forward log events to the telemetry provider (using the provider's logging methods).

Example
python
Copy
Download
from kernel.diagnostics import Diagnostics, DiagnosticsRegistry
from kernel.events import EventBus
from kernel.providers import TelemetryProvider

event_bus = EventBus()
telemetry = TelemetryProvider()  # or a concrete implementation
registry = DiagnosticsRegistry()

diag = Diagnostics(event_bus, telemetry_provider=telemetry, registry=registry)
diag.start()

# Later
health = diag.health()
metrics = diag.metrics()
traces = diag.traces(limit=10)

diag.stop()
