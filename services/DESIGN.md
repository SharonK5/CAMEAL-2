# Services Design

## Philosophy

Execution stages should contain orchestration only.

Business logic belongs to services.

This keeps workflow independent from implementation.

---

## Service Lifecycle

```
Create

↓

Initialize

↓

Execute

↓

Shutdown
```

---

## Service Contract

Every service implements:

- name
- initialize()
- shutdown()

Domain services extend this contract.

---

## Dependency Injection

Execution stages receive services through constructor injection.

Example:

```
AnalyticsStage

↓

AnalyticsService
```

This enables:

- Testing
- Mocking
- Swappable implementations

---

## Stateless Design

Services should be stateless whenever possible.

Shared runtime information belongs in ExecutionContext.

Persistent information belongs in repositories.

---

## Error Handling

Services throw service-specific exceptions.

Execution stages translate failures into StageResult objects.

---

## Future Extensions

- Service versioning
- Service capabilities
- Plugin discovery
- Distributed services
- Cloud-native execution
