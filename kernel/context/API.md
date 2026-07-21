# CAMEAL Kernel Events API

**Package:** `cameal.kernel.events`  
**Version:** 1.0.0  
**Status:** Stable Public API

---

# Overview

The Events subsystem provides the event-driven communication backbone of the
CAMEAL Kernel.

It enables loosely coupled communication between runtime components using
immutable events, publish/subscribe messaging, event routing, filtering,
validation, and synchronous or asynchronous execution pipelines.

The Events subsystem is transport-agnostic and contains no domain-specific
logic.

---

# Public API

The following classes form the stable public API.

| Class | Description | Stability |
|---------|-------------|-----------|
| Event | Immutable event object | Stable |
| EventBus | Publish/Subscribe interface | Stable |
| Dispatcher | Dispatches events to subscribers | Stable |
| Subscriber | Base subscriber contract | Stable |
| EventFilter | Filters events | Stable |
| ExecutionPipeline | Executes event pipelines | Stable |

Public APIs follow semantic versioning.

Breaking changes will only occur in major versions.

---

# Core Concepts

```
Publisher
     │
     ▼
 EventBus
     │
     ▼
 Dispatcher
     │
     ▼
 Event Filters
     │
     ▼
 Subscribers
```

---

# Event

Immutable runtime event.

```python
Event(
    event_type="request.received",
    payload={"user": "alice"},
    source="gateway"
)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| event_id | UUID | Unique identifier |
| event_type | str | Event type |
| payload | dict | Event payload |
| priority | EventPriority | Processing priority |
| timestamp | datetime | UTC creation timestamp |
| source | str | Publisher |
| correlation_id | str | Workflow correlation |
| metadata | dict | Additional metadata |

---

# EventBus

Central publish/subscribe interface.

## Publish

```python
event_bus.publish(event)
```

## Subscribe

```python
event_bus.subscribe(
    "request.received",
    subscriber
)
```

## Unsubscribe

```python
event_bus.unsubscribe(
    "request.received",
    subscriber
)
```

---

# Dispatcher

Routes events to matching subscribers.

Responsibilities

- ordering
- prioritisation
- filtering
- dispatch execution
- subscriber invocation

```python
dispatcher.dispatch(event)
```

---

# Subscriber

Base subscriber interface.

```python
class Subscriber:

    def handle(
        self,
        event: Event
    ) -> None:
        ...
```

Subscribers should

- remain stateless
- avoid blocking operations
- raise meaningful exceptions
- be idempotent whenever possible

---

# EventFilter

Filters determine whether an event should reach a subscriber.

Examples

```python
ByTypeFilter("security.authenticated")

BySourceFilter("kernel")

PayloadFilter("tenant")
```

Filters may be combined.

```python
CompositeFilter(
    ByTypeFilter(...),
    BySourceFilter(...)
)
```

---

# ExecutionPipeline

Coordinates execution.

Supports

- synchronous execution
- asynchronous execution
- priority ordering
- filter evaluation
- subscriber invocation

```python
pipeline.execute(event)
```

---

# Event Priorities

| Priority | Description |
|-----------|-------------|
| CRITICAL | Immediate execution |
| HIGH | High priority |
| NORMAL | Default |
| LOW | Deferred |
| BACKGROUND | Lowest priority |

---

# Event Lifecycle

```
Create Event
      │
      ▼
Validate
      │
      ▼
Publish
      │
      ▼
Dispatch
      │
      ▼
Filter
      │
      ▼
Subscribers
      │
      ▼
Complete
```

---

# Serialization

Events support serialization.

```python
event.to_dict()

event.to_json()

Event.from_dict(data)

Event.from_json(data)
```

---

# Validation

Events are validated before publication.

Validation includes

- event type
- payload structure
- metadata
- timestamp
- identifiers

Invalid events raise

```
EventValidationError
```

---

# Thread Safety

The Events subsystem supports concurrent publishing.

Guarantees

- immutable events
- thread-safe subscriber registry
- deterministic dispatch ordering
- isolated subscriber execution

---

# Error Handling

Primary exceptions

```python
EventError

EventValidationError

DispatchError

SubscriberError

PipelineError
```

Errors are propagated to the caller unless handled by the execution pipeline.

---

# Extension Points

Applications may extend the subsystem by implementing:

- custom subscribers
- custom filters
- custom dispatchers
- custom execution pipelines
- custom event validators

The core Event contract must not be modified.

---

# Semantic Versioning

Current Version

```
1.0.0
```

Public API Stability

| Component | Status |
|-----------|--------|
| Event | Stable |
| EventBus | Stable |
| Dispatcher | Stable |
| Subscriber | Stable |
| EventFilter | Stable |
| ExecutionPipeline | Stable |

Internal classes are **not** covered by semantic version guarantees.

---

# Best Practices

- Prefer immutable payloads.
- Keep events small and self-contained.
- Use correlation IDs for workflow tracing.
- Design subscribers to be idempotent.
- Avoid long-running work inside subscribers.
- Publish events only after successful validation.
- Use filters to reduce unnecessary dispatching.
- Treat events as historical facts, not mutable state.

---

# Example

```python
from cameal.kernel.events import Event, EventBus

bus = EventBus()

event = Event(
    event_type="document.ingested",
    payload={
        "document_id": "DOC-001",
        "repository": "knowledge"
    },
    source="repository"
)

bus.publish(event)
```

---

# Compatibility

| Version | Compatibility |
|----------|---------------|
| 1.x | Fully compatible |
| 2.x | May introduce breaking changes |

Applications should depend only on the documented public API.
