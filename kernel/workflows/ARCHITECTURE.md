### `kernel/workflows/ARCHITECTURE.md`

```markdown
# Workflows Architecture

## High-Level Design
┌─────────────────────────────────────────────────────────┐
│ Kernel Runtime │
│ │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Workflow Subsystem │ │
│ │ │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────────┐ │ │
│ │ │ Parser │───▶│ Planner │───▶│ Executor │ │ │
│ │ └─────────┘ └─────────┘ └─────────────┘ │ │
│ │ │ │ │ │ │
│ │ ▼ ▼ ▼ │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────────┐ │ │
│ │ │Registry │ │Validator│ │ResultCollect│ │ │
│ │ └─────────┘ └─────────┘ └─────────────┘ │ │
│ └─────────────────────────────────────────────────┘ │
│ │ │
│ ┌──────────────────────▼───────────────────────┐ │
│ │ Orchestrator │ │
│ └──────────────────────┬───────────────────────┘ │
│ │ │
│ ┌──────────────────────▼───────────────────────┐ │
│ │ Plugin Manager │ │
│ └──────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘

text
Copy
Download

## Components

### 1. Parser
- Parses YAML/JSON workflow definitions
- Validates structural correctness
- Returns `Workflow` objects

### 2. Registry
- Thread-safe storage of workflows
- Supports default workflow selection
- Enables runtime discovery

### 3. Planner
- Resolves dependencies between steps
- Builds an execution plan (ordered graph)
- Validates execution order

### 4. Validator
- Checks workflow semantics
- Detects circular dependencies
- Validates plugin references

### 5. Executor
- Executes the execution plan
- Coordinates step execution
- Collects and aggregates results

### 6. Result Collector
- Aggregates results from all steps
- Handles failures gracefully
- Returns a consolidated result

## Data Flow
YAML/JSON
│
▼
Parser
│
▼
Workflow
│
▼
Validator
│
▼
Registry
│
▼
Planner
│
▼
ExecutionPlan
│
▼
Executor
│
▼
Result

text
Copy
Download

## Dependencies

- Workflows depend on the kernel's `Lifecycle` and `Event` systems.
- Workflows do NOT depend on providers, engines, or domain logic.
- Workflows are consumed by the `Orchestrator`.

## Extension Points

- New parsers (TOML, HCL, etc.)
- Custom validators
- Alternative planners (parallel, conditional, etc.)
- Execution hooks
