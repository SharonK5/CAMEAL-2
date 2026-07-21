# CAMEAL Kernel Events API

**Package:** `cameal.kernel.events`

**Version:** 1.0.0

**API Status:** Stable

---

# Overview

The Events subsystem provides the event-driven communication infrastructure for the CAMEAL Kernel.

Its responsibilities are to:

- publish events
- subscribe to events
- dispatch events
- propagate execution context
- coordinate synchronous and asynchronous execution
- provide observability through tracing and metrics

The Events subsystem contains **no business logic**. It transports events between runtime components.

---

# API Stability

The Events subsystem follows Semantic Versioning.

| API | Status |
|------|---------|
| Public API | Stable |
| Internal API | Private |
| Experimental API | Explicitly marked |

Public interfaces maintain backwards compatibility within the same major version.

---

# Public API

The following classes form the supported public contract.

| Class | Purpose |
|---------|---------|
| Event | Immutable event object |
| EventBus | Publish/subscribe runtime |
| Publisher | Creates and publishes events |
| Subscriber | Base subscriber interface |
| Subscription | Subscription metadata |
| EventContext | Event execution context |

Everything else is considered internal.

---

# Event

Represents an immutable runtime event.

```python
class Event:
    ...
```

## Responsibilities

- immutable payload
- timestamp
- correlation identifiers
- event metadata
- provenance
- priority

---

## Required Properties

```python
event.id

event.type

event.timestamp

event.source

event.context

event.payload

event.metadata
```

---

# EventBus

Primary communication mechanism inside the kernel.

```python
bus = EventBus()
```

---

## publish()

Publishes an event.

```python
bus.publish(event)
```

Returns

```
None
```

Raises

```
EventError
```

---

## subscribe()

Registers a subscriber.

```python
bus.subscribe(
    subscriber,
    event_type="ReasoningCompleted"
)
```

---

## unsubscribe()

Removes a subscriber.

```python
bus.unsubscribe(subscriber)
```

---

# Publisher

Creates and emits events.

```python
publisher.publish(event)
```

Publishers never invoke subscribers directly.

---

# Subscriber

Base class for all subscribers.

```python
class Subscriber:
```

Required method

```python
handle(event)
```

Returns

```
None
```

Subscribers should be stateless whenever possible.

---

# Subscription

Represents registration metadata.

Properties

```
subscriber

event_type

priority

filter

enabled
```

---

# EventContext

Carries execution state throughout the event pipeline.

Contains

```
request_id

correlation_id

workflow_id

user

trace

provenance

metadata
```

EventContext is immutable.

Each stage returns a new context.

---

# Supported Event Types

Kernel lifecycle

```
KernelInitializing

KernelInitialized

KernelStarting

KernelStarted

KernelStopping

KernelStopped
```

---

Workflow

```
WorkflowSelected

WorkflowStarted

WorkflowCompleted

WorkflowFailed
```

---

Execution

```
RequestReceived

ContextCreated

ExecutionStarted

ExecutionCompleted

ExecutionFailed
```

---

Security

```
SecurityStarted

SecurityCompleted

SecurityDenied
```

---

Retrieval

```
RetrievalStarted

RetrievalCompleted

RetrievalFailed
```

---

Reasoning

```
ReasoningStarted

ReasoningCompleted

ReasoningFailed
```

---

Monitoring

```
MonitoringStarted

MonitoringCompleted
```

---

Evaluation

```
EvaluationStarted

EvaluationCompleted
```

---

Accountability

```
AccountabilityStarted

AccountabilityCompleted
```

---

Learning

```
LearningStarted

LearningCompleted
```

---

Adaptation

```
AdaptationStarted

AdaptationCompleted
```

---

Response

```
ResponseBuilt

ResponseSent
```

---

Diagnostics

```
MetricRecorded

TraceRecorded

AuditRecorded

HealthChanged
```

---

# Event Ordering

The kernel guarantees deterministic ordering for synchronous workflows.

```
RequestReceived

↓

ContextCreated

↓

WorkflowSelected

↓

SecurityStarted

↓

RetrievalStarted

↓

ReasoningStarted

↓

MonitoringStarted

↓

EvaluationStarted

↓

AccountabilityStarted

↓

LearningStarted

↓

AdaptationStarted

↓

ResponseBuilt
```

Background events may execute asynchronously.

---

# Event Priorities

Supported priorities

```
CRITICAL

HIGH

NORMAL

LOW

BACKGROUND
```

Priority determines dispatch order.

---

# Error Handling

Possible exceptions

```
EventError

ValidationError

DispatchError

SubscriberError

SerializationError
```

Errors are propagated to the dispatcher.

Subscribers should never terminate the EventBus.

---

# Thread Safety

The EventBus is thread-safe.

The implementation guarantees

- safe concurrent publishing
- concurrent subscribers
- immutable events
- isolated execution contexts

---

# Compatibility

Stable API

```
Event

EventBus

Publisher

Subscriber

Subscription

EventContext
```

Internal implementation

```
Dispatcher

Registry

Middleware

Validator

Filters

Serializer

Diagnostics
```

These components may change without notice.

---

# Versioning

```
Major

breaking API changes
```

```
Minor

new backwards-compatible functionality
```

```
Patch

bug fixes and performance improvements
```

Current Version

```
1.0.0
```

API Version

```
1.0
```

Status

```
Stable
```
