# Diagnostics Design

## Design Principles

The diagnostics subsystem is designed around four principles:

1. **Non‑invasive** – diagnostics does not change the behaviour of other subsystems. It only observes.
2. **Observability first** – all components are assumed to emit events and provide health. Diagnostics is the consumer.
3. **Correlation** – every diagnostic event includes correlation IDs (trace_id, span_id, request_id) so logs and traces can be joined.
4. **Extensible** – new health checks, metrics, and trace filters can be added via the registry without changing core code.

## Design Decisions

### 1. Event‑Driven Observation

All diagnostics data flows through the EventBus. This avoids tight coupling and allows future subsystems to emit diagnostic data without knowing about Diagnostics.

### 2. In‑Memory Storage with Limits

Traces and logs are stored in‑memory with configurable limits (default: 100 traces, 500 logs). This keeps diagnostics lightweight and avoids external dependencies. For long‑term storage, the Diagnostics API can be extended to export data.

### 3. Synchronous Logging

Logs are emitted synchronously to the TelemetryProvider. If the TelemetryProvider is configured for asynchronous delivery, that is handled at that layer.

### 4. Health on Demand

Health is checked on demand, not periodically. This avoids unnecessary network calls and allows the application to check health at its own frequency (e.g., via an API endpoint).

## Trade‑Offs

| Decision                | Benefit                                      | Trade‑Off                                  |
|-------------------------|----------------------------------------------|--------------------------------------------|
| Event‑driven            | Loose coupling, future‑proof                | Depends on a fully functional EventBus     |
| In‑memory storage       | Simple, no external dependencies            | Limited history (configurable)             |
| Synchronous logging     | Consistent ordering, no buffer loss         | Can block the calling thread               |
| Health on demand        | Lightweight, flexible                       | Health may be stale between checks         |

## Security Considerations

- Diagnostic data should not contain secrets or sensitive information.
- If logs or traces contain sensitive data, they should be redacted by the source component before emitting.

## Performance Considerations

- Subscribing to all events on the EventBus (`*`) is acceptable because Diagnostics only does lightweight processing (store or emit).
- The trace limit prevents unbounded memory growth.
- Health checks should be fast (avoid network calls, disk I/O, etc.) to ensure quick responses.
