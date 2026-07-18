# CAMEAL Kernel API

## Purpose

This document defines the public programming interface of the CAMEAL Kernel.

Only the interfaces described here are considered stable.

Internal managers, containers, registries, and workflows are implementation details and must not be accessed directly.

---

# Primary Class

```
CAMEALKernel
```

The kernel is the runtime entry point of the platform.

---

# Construction

```python
kernel = CAMEALKernel(config)
```

Parameters

| Name | Type | Description |
|------|------|-------------|
| config | Config | Runtime configuration |

---

# Lifecycle API

## initialize()

Initializes all runtime managers.

Returns

```
None
```

---

## validate()

Validates

- configuration
- plugins
- dependencies
- repositories
- engines

Raises

```
KernelValidationError
```

---

## boot()

Bootstraps the runtime.

Responsibilities

- load plugins
- register repositories
- register engines
- build workflows

---

## start()

Starts all managed components.

Returns

```
None
```

---

## execute(request)

Executes a workflow.

Input

```
Request
```

Output

```
Response
```

Raises

```
ExecutionError
```

---

## stop()

Gracefully stops execution.

---

## shutdown()

Releases all resources.

---

## dispose()

Removes internal references.

---

## health()

Returns

```
HealthStatus
```

Example

```python
status = kernel.health()

print(status.overall)
```

---

# Request

```
Request
```

Fields

```
request_id

identity

resource

operation

context

metadata

environment

session
```

---

# Response

```
Response
```

Contains

```
decision

evidence

provenance

metrics

execution_time

trace

recommendations
```

---

# Bootstrap

```
Bootstrap.bootstrap(config)
```

Creates

```
Kernel
```

---

# Managers

The following managers are available internally.

```
EngineManager

RepositoryManager

WorkflowManager

ContextManager

Scheduler

PluginLoader
```

Applications should not access these directly.

---

# Events

The kernel publishes

```
KernelStarted

KernelStopped

RequestReceived

WorkflowStarted

WorkflowCompleted

ExecutionFailed

HealthChanged
```

---

# Exceptions

Primary exceptions

```
KernelError

ConfigurationError

ValidationError

ExecutionError

DependencyError

PluginError
```

---

# Thread Safety

The kernel is thread-safe.

Requests may execute concurrently.

Execution contexts remain immutable.

---

# Stability

Everything documented in this file is considered part of the public API.

Anything else is considered internal implementation.
