# kernel/workflows/base/exceptions.py
"""
Workflow-specific exceptions.
"""


class WorkflowError(Exception):
    """Base exception for all workflow errors."""
    pass


class WorkflowNotFoundError(WorkflowError):
    """Raised when a requested workflow is not found."""
    pass


class WorkflowValidationError(WorkflowError):
    """Raised when a workflow definition is invalid."""
    pass


class WorkflowExecutionError(WorkflowError):
    """Raised when a workflow execution fails."""
    pass


class StepNotFoundError(WorkflowError):
    """Raised when a referenced step is not found."""
    pass


class StepExecutionError(WorkflowError):
    """Raised when a step execution fails."""
    pass
