# CAMEAL Kernel Workflows

## Overview

Workflows are declarative execution specifications that define the order, dependencies, and conditions for executing plugins.

The workflow subsystem provides:

- **Definition** – YAML/JSON declarations of execution sequences
- **Validation** – Structural and semantic validation of workflow definitions
- **Planning** – Dependency resolution and execution plan generation
- **Execution** – Coordinated execution of workflow steps
- **Lifecycle** – Integration with the kernel's lifecycle management

Workflows contain **no domain logic**. They are purely declarative specifications.

## Key Concepts

- **Workflow** – A named collection of steps with execution order
- **Step** – A single execution unit referencing a plugin
- **Plugin** – The component that provides the actual execution logic
- **Execution Plan** – An ordered, dependency-resolved plan for execution

## Relationship with Other Subsystems

- **Plugins** – Workflows invoke plugins for actual execution
- **Orchestrator** – Executes the workflow's execution plan
- **Providers** – Invisible to workflows; used by plugins
- **Scheduler** – Schedules workflow execution

## Getting Started

Define a workflow in YAML:

```yaml
name: document_analysis
version: 1.0
description: Analyze a document
steps:
  - name: context
    plugin: context
  - name: retrieve
    plugin: repository
  - name: analyze
    plugin: reasoning
  - name: report
    plugin: drafting
