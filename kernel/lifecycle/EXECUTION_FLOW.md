markdown
Copy
Download
# CAMEAL Kernel Lifecycle – Execution Flow

## Overview

This document describes the execution flow of the Lifecycle subsystem: how components transition between states, how the LifecycleManager orchestrates startup and shutdown, and how failures are handled.

The flow is deterministic, observable, and validated at every step.

---

## State Transition Flow

### Normal Flow (No Failures)
CREATED
│
▼
INITIALIZED (initialize())
│
▼
VALIDATED (validate())
│
▼
BOOTED (boot())
│
▼
STARTED (start())
│
▼
RUNNING (run)
│
▼
STOPPING (stop())
│
▼
STOPPED
│
▼
SHUTDOWN (shutdown())
│
▼
DISPOSED (dispose())

text
Copy
Download

### Optional Pause/Resume (for components implementing Pausable)
RUNNING
│
├─────────────► PAUSED (pause())
│ │
│ ▼
│ RESUMED (resume())
│ │
│ ▼
└─────────────────► RUNNING

text
Copy
Download

### Failure Flow (Any State)
Any State
│
▼
FAILED (fail())
│
▼
DISPOSED (dispose())

text
Copy
Download

---

## Startup Sequence

The LifecycleManager starts components in **registration order**.
LifecycleManager.start_all()
│
▼
┌───────────────────────────────────────────────────────────────┐
│ For each component in registration order: │
│ │
│ 1. comp.initialize() ──────► INITIALIZED │
│ 2. comp.validate() ──────► VALIDATED │
│ 3. comp.boot() ──────► BOOTED │
│ 4. comp.start() ──────► RUNNING │
│ │
└───────────────────────────────────────────────────────────────┘
│
▼
All components are RUNNING.

text
Copy
Download

### Example: Three Components
Registration Order: A, B, C

A.initialize() → A.INITIALIZED
A.validate() → A.VALIDATED
A.boot() → A.BOOTED
A.start() → A.RUNNING

B.initialize() → B.INITIALIZED
B.validate() → B.VALIDATED
B.boot() → B.BOOTED
B.start() → B.RUNNING

C.initialize() → C.INITIALIZED
C.validate() → C.VALIDATED
C.boot() → C.BOOTED
C.start() → C.RUNNING

text
Copy
Download

---

## Shutdown Sequence

Shutdown occurs in **reverse registration order**.
LifecycleManager.stop_all()
│
▼
┌───────────────────────────────────────────────────────────────┐
│ For each component in reverse registration order: │
│ │
│ 1. comp.stop() ──────► STOPPING → STOPPED │
│ 2. comp.shutdown() ──────► SHUTDOWN │
│ 3. comp.dispose() ──────► DISPOSED │
│ │
└───────────────────────────────────────────────────────────────┘
│
▼
All components are DISPOSED.

text
Copy
Download

### Example: Three Components
Registration Order: A, B, C
Shutdown Order: C, B, A

C.stop() → C.STOPPED
C.shutdown() → C.SHUTDOWN
C.dispose() → C.DISPOSED

B.stop() → B.STOPPED
B.shutdown() → B.SHUTDOWN
B.dispose() → B.DISPOSED

A.stop() → A.STOPPED
A.shutdown() → A.SHUTDOWN
A.dispose() → A.DISPOSED

text
Copy
Download

---

## Failure Flow

If a component fails during any transition:
Component catches exception.

Component calls self.fail(error).

Component state becomes FAILED.

LifecycleManager logs the failure.

LifecycleManager publishes ComponentFailed event.

LifecycleManager continues with remaining components.

text
Copy
Download

### Example: Component B Fails During `start()`
A.initialize() → A.INITIALIZED
A.validate() → A.VALIDATED
A.boot() → A.BOOTED
A.start() → A.RUNNING

B.initialize() → B.INITIALIZED
B.validate() → B.VALIDATED
B.boot() → B.BOOTED
B.start() → ❌ EXCEPTION ❌
│
▼
B.fail(error) → B.FAILED
│
▼
LifecycleManager logs: "B failed during start"
LifecycleManager publishes: ComponentFailed(B, error)

C.initialize() → C.INITIALIZED
C.validate() → C.VALIDATED
C.boot() → C.BOOTED
C.start() → C.RUNNING

Result: A and C are RUNNING; B is FAILED.

text
Copy
Download

---

## Health Aggregation Flow
LifecycleManager.health_all()
│
▼
┌───────────────────────────────────────────────────────────────┐
│ For each component: │
│ │
│ 1. Call comp.health_report() │
│ 2. Collect report │
│ │
└───────────────────────────────────────────────────────────────┘
│
▼
Return Dict[str, HealthReport]

text
Copy
Download

### Health Report Example

```json
{
  "Kernel": {
    "component": "Kernel",
    "state": "RUNNING",
    "healthy": true,
    "uptime": 1234.5,
    "version": "1.0.0",
    "message": "Operational"
  },
  "Container": {
    "component": "Container",
    "state": "RUNNING",
    "healthy": true,
    "uptime": 1234.5,
    "version": "1.0.0",
    "message": "Operational"
  },
  "ReasoningEngine": {
    "component": "ReasoningEngine",
    "state": "RUNNING",
    "healthy": false,
    "uptime": 1234.5,
    "version": "1.0.0",
    "message": "Health: UNHEALTHY",
    "details": {
      "error": "Connection to LLM service failed"
    }
  }
}
Lifecycle Event Flow
Every transition publishes an event.

text
Copy
Download
┌───────────────────────────────────────────────────────────────┐
│ Lifecycle Event Flow                                         │
│                                                               │
│ Component.initialize()  → ComponentInitialized               │
│ Component.validate()    → ComponentValidated                 │
│ Component.boot()        → ComponentBooted                    │
│ Component.start()       → ComponentStarted                   │
│ Component.stop()        → ComponentStopped                   │
│ Component.shutdown()    → ComponentShutdown                  │
│ Component.dispose()     → ComponentDisposed                  │
│ Component.fail()        → ComponentFailed                    │
└───────────────────────────────────────────────────────────────┘
Event Subscribers
Logging → Records every transition.

Monitoring → Updates metrics and health dashboard.

Audit → Records transitions for compliance.

Event Bus → Forwards events to interested subsystems.

Error Handling Sequence
text
Copy
Download
Error Occurred
    │
    ▼
Component catches error
    │
    ├─────────────────────────────────────────────────────────────────┐
    │                                                                 │
    ▼                                                                 ▼
If transition is invalid:                                     If component logic fails:
LifecycleError raised                                          Component.fail(error)
    │                                                                 │
    ▼                                                                 ▼
Manager logs error                                             State becomes FAILED
    │                                                                 │
    ▼                                                                 ▼
Execution continues?                                          Manager continues with
                                                              remaining components
Invalid Transition Example
python
Copy
Download
# Component is CREATED
comp = MyComponent()

# Attempting to start without initializing
try:
    comp.start()
except LifecycleError as e:
    # e: "Invalid transition from created to started"
    pass
Runtime Guarantees in Action
Guarantee	Implementation
Valid transitions only	Every _transition() call checks transitions.is_valid_transition().
Deterministic startup	Components are started in registration order.
Deterministic shutdown	Components are stopped in reverse registration order.
Health reporting	health_report() is called for each component.
Event publication	Each transition emits an event.
Idempotent shutdown	Multiple calls to stop() are safe.
Resource cleanup	dispose() is called on all components.
Summary
The execution flow is:

Startup → components initialize → validate → boot → start → run.

Runtime → components run, periodically report health.

Shutdown → components stop → shutdown → dispose (reverse order).

Failure → any component can fail, transitioning to FAILED; other components continue.

This flow ensures predictable, observable, and resilient execution for all kernel-managed components.

text
Copy
Download

---

This `EXECUTION_FLOW.md` is now complete. It describes the state transitions, startup/shutdown sequences, failure handling, health aggregation, and event flow in detail, making it a valuable reference for developers working with the Lifecycle subsystem.
