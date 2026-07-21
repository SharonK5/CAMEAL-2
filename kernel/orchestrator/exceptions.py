# kernel/orchestrator/exceptions.py
"""
Orchestrator-specific exceptions.
"""

class OrchestratorError(Exception):
    """Base exception for orchestrator errors."""
    pass


class PlanValidationError(OrchestratorError):
    """Raised when an execution plan fails validation."""
    pass


class WorkflowNotFoundError(OrchestratorError):
    """Raised when a requested workflow does not exist."""
    pass


class EngineNotFoundError(OrchestratorError):
    """Raised when a requested engine is not registered."""
    pass


class ExecutionError(OrchestratorError):
    """Raised when an engine execution fails."""
    pass


class DispatcherError(OrchestratorError):
    """Raised when the dispatcher fails to invoke an engine."""
    pass
