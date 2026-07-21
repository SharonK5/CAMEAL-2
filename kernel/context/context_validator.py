# kernel/context/context_validator.py
"""
Context validator – validates context integrity.
"""

from .execution_context import ExecutionContext
from .exceptions import ContextValidationError


class ContextValidator:
    """
    Validates execution contexts.
    """

    def validate(self, context: ExecutionContext) -> None:
        """Validate the execution context."""
        if not context.request:
            raise ContextValidationError("Request context is required")

        if not context.request.identity:
            raise ContextValidationError("Identity is required")

        if not context.request.operation:
            raise ContextValidationError("Operation is required")

        # Validate trace if present
        if context.trace.trace_id:
            if not context.trace.span_id:
                raise ContextValidationError("Span ID required when trace ID is present")
