# kernel/workflows/events/workflow_events.py
"""
Workflow event definitions.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class WorkflowStarted:
    """Event emitted when a workflow starts execution."""
    workflow_name: str
    context: Dict[str, Any]


@dataclass
class WorkflowCompleted:
    """Event emitted when a workflow completes successfully."""
    workflow_name: str
    results: Dict[str, Any]
    execution_time: float


@dataclass
class WorkflowFailed:
    """Event emitted when a workflow fails."""
    workflow_name: str
    errors: Dict[str, str]
    execution_time: float


@dataclass
class StepStarted:
    """Event emitted when a step starts execution."""
    workflow_name: str
    step_name: str


@dataclass
class StepCompleted:
    """Event emitted when a step completes."""
    workflow_name: str
    step_name: str
    result: Any


@dataclass
class StepFailed:
    """Event emitted when a step fails."""
    workflow_name: str
    step_name: str
    error: str
