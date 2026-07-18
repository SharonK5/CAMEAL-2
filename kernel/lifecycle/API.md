markdown
Copy
Download
# CAMEAL Kernel Lifecycle – API

## Purpose

This document defines the public programming interface of the CAMEAL Kernel Lifecycle subsystem.

Only the interfaces described here are considered stable.

Internal classes (e.g., TransitionValidator, EventPublisher) are implementation details and must not be accessed directly.

---

## Public Components
Lifecycle
Pausable
LifecycleManager
LifecycleState
HealthStatus
HealthReport
LifecycleObserver
NullObserver
Diagnostics
LifecycleError

text
Copy
Download

---

## Lifecycle

Abstract base class for all kernel-managed components.

### Methods

| Method | Description | Raises |
|--------|-------------|--------|
| `initialize()` | Allocate resources (connections, threads, caches). | `LifecycleError` if state not `CREATED`. |
| `validate()` | Validate configuration and dependencies. | `LifecycleError` if state not `INITIALIZED`. |
| `boot()` | Boot the component (load plugins, register endpoints). | `LifecycleError` if state not `VALIDATED`. |
| `start()` | Begin accepting work. Transitions to `STARTED` then `RUNNING`. | `LifecycleError` if state not `BOOTED`. |
| `stop()` | Gracefully stop execution. | `LifecycleError` if state not `RUNNING` or `PAUSED`. |
| `shutdown()` | Release resources. | `LifecycleError` if state not `STOPPED`. |
| `dispose()` | Final cleanup. | `LifecycleError` if state not `SHUTDOWN`. |
| `fail(error)` | Mark component as `FAILED`. | None. |
| `health()` | Return current health status. | None. |
| `health_report()` | Return detailed health report. | None. |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `state` | `LifecycleState` | Current lifecycle state. |
| `version` | `str` (optional) | Component version (if overridden). |

### Example

```python
from cameal.kernel.lifecycle import Lifecycle, HealthStatus

class MyEngine(Lifecycle):
    def _on_initialize(self):
        # allocate resources
        pass

    def _on_health(self) -> HealthStatus:
        return HealthStatus.HEALTHY
Pausable
Optional interface for components that support pausing and resuming.

Methods
Method	Description	Raises
pause()	Temporarily pause execution.	LifecycleError if state not RUNNING.
resume()	Resume execution after pause.	LifecycleError if state not PAUSED.
Example
python
Copy
Download
from cameal.kernel.lifecycle import Lifecycle, Pausable

class PausableEngine(Lifecycle, Pausable):
    def pause(self):
        # pause logic
        pass

    def resume(self):
        # resume logic
        pass
LifecycleManager
Orchestrates lifecycle of all registered components.

Methods
Method	Description
register(component)	Register a lifecycle component.
unregister(component)	Remove a component.
initialize_all()	Initialize all components in registration order.
validate_all()	Validate all components.
boot_all()	Boot all components.
start_all()	Start all components.
pause_all()	Pause all components that implement Pausable.
resume_all()	Resume all paused components that implement Pausable.
stop_all()	Stop all components in reverse order.
shutdown_all()	Shutdown all components.
dispose_all()	Dispose all components.
health_all()	Return aggregated health reports for all components.
diagnostics_all()	Return diagnostic information for all components.
add_observer(observer)	Add a lifecycle observer.
remove_observer(observer)	Remove a lifecycle observer.
Exceptions
LifecycleError – if a component fails during lifecycle orchestration.

Example
python
Copy
Download
from cameal.kernel.lifecycle import LifecycleManager, Lifecycle

manager = LifecycleManager()
manager.register(my_engine)
manager.initialize_all()
manager.start_all()
LifecycleState
Enumeration of valid lifecycle states.

Member	Value	Description
CREATED	"created"	Component constructed.
INITIALIZED	"initialized"	Resources allocated.
VALIDATED	"validated"	Configuration validated.
BOOTED	"booted"	Bootstrapped.
STARTED	"started"	Ready to accept work.
RUNNING	"running"	Fully operational.
STOPPING	"stopping"	Graceful shutdown in progress.
STOPPED	"stopped"	Gracefully stopped.
SHUTDOWN	"shutdown"	Resources released.
DISPOSED	"disposed"	Final cleanup complete.
FAILED	"failed"	Terminal error state.
HealthStatus
Enumeration of health statuses.

Member	Value	Description
HEALTHY	"healthy"	Fully operational.
DEGRADED	"degraded"	Operational with reduced capacity.
UNHEALTHY	"unhealthy"	Not operational.
UNKNOWN	"unknown"	Status cannot be determined.
HealthReport
Detailed health report for a component.

Attributes
Attribute	Type	Description
component	str	Component name.
state	LifecycleState	Current lifecycle state.
healthy	bool	True if healthy.
timestamp	datetime	Report timestamp (UTC).
uptime	float (optional)	Uptime in seconds.
version	str (optional)	Component version.
message	str	Status message.
details	dict	Additional details.
Methods
Method	Description
status	Returns HealthStatus derived from healthy.
to_dict()	Converts to dictionary for serialisation.
LifecycleObserver
Interface for lifecycle event observers.

Methods
Method	Description
on_initialized(component)	Called after component initialized.
on_validated(component)	Called after component validated.
on_booted(component)	Called after component booted.
on_started(component)	Called after component started.
on_stopped(component)	Called after component stopped.
on_shutdown(component)	Called after component shutdown.
on_disposed(component)	Called after component disposed.
on_failed(component, error)	Called when component fails.
on_health_changed(component, report)	Called when component health changes.
Example
python
Copy
Download
from cameal.kernel.lifecycle import LifecycleObserver

class MyObserver(LifecycleObserver):
    def on_started(self, component):
        print(f"{component} started")
NullObserver
No‑op observer for convenience.

Implements all LifecycleObserver methods as no‑ops.

Diagnostics
Provides diagnostics aggregation.

Methods
Method	Description
aggregate(reports)	Aggregates health reports into a single dictionary with overall health, component counts, and individual reports.
Returns
Field	Type	Description
overall	str	"healthy", "degraded", or "unhealthy".
healthy	int	Count of healthy components.
degraded	int	Count of degraded components.
unhealthy	int	Count of unhealthy components.
unknown	int	Count of components with unknown health.
total	int	Total number of components.
components	list	List of component health report dictionaries.
Example
python
Copy
Download
from cameal.kernel.lifecycle import Diagnostics

reports = manager.health_all()
summary = Diagnostics.aggregate(reports)
print(summary["overall"])
LifecycleError
Exception raised for invalid lifecycle transitions.

Attributes
Attribute	Type	Description
current_state	str (optional)	Current lifecycle state when error occurred.
target_state	str (optional)	Target state that was attempted.
Usage
python
Copy
Download
try:
    component.start()
except LifecycleError as e:
    print(f"Invalid transition: {e}")
API Stability
The following APIs are considered stable and will not change without a major version increment:

Lifecycle

Pausable

LifecycleManager

LifecycleState

HealthStatus

HealthReport

LifecycleObserver

NullObserver

Diagnostics

LifecycleError

All other classes and functions are internal and subject to change without notice.

Versioning
Public API version: 1.0.0

Semantic versioning applies (MAJOR.MINOR.PATCH)

Backward‑incompatible changes increment MAJOR

New features increment MINOR

Bug fixes increment PATCH

Example Usage
python
Copy
Download
from cameal.kernel.lifecycle import (
    Lifecycle,
    LifecycleManager,
    LifecycleState,
    HealthStatus,
    LifecycleObserver,
    Diagnostics,
)

class MyEngine(Lifecycle):
    def __init__(self):
        super().__init__()
        self._healthy = True

    def _on_initialize(self):
        # allocate resources
        pass

    def _on_health(self) -> HealthStatus:
        return HealthStatus.HEALTHY if self._healthy else HealthStatus.UNHEALTHY

manager = LifecycleManager()
engine = MyEngine()
manager.register(engine)

manager.initialize_all()
manager.start_all()

# Health check
report = manager.health_all()["MyEngine"]
print(report.healthy)  # True

# Shutdown
manager.stop_all()
manager.shutdown_all()
manager.dispose_all()
