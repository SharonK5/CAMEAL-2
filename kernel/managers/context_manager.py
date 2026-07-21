# kernel/managers/context_manager.py
"""
Context Manager – builds and propagates execution context.
"""

from typing import Any, Dict, Optional
from ..models import Request, ExecutionContext
from ..context import ContextBuilder, ContextValidator
from .manager import Manager
from .exceptions import ManagerValidationError, ManagerError


class ContextManager(Manager):
    """
    Manages execution context.

    Responsibilities:
        - Create an execution context from a request.
        - Enrich context with additional data.
        - Validate context.
        - Persist context (optional).
    """

    def __init__(self) -> None:
        super().__init__("context_manager")
        self._builder = ContextBuilder()
        self._validator = ContextValidator()

    def build(self, request: Request) -> ExecutionContext:
        """Create an execution context from a request."""
        if not request:
            raise ManagerValidationError("Request cannot be None")

        ctx = (
            self._builder
            .with_request(
                identity=request.identity,
                resource=request.resource,
                operation=request.operation,
                metadata=request.metadata,
                environment=request.environment,
                session=request.session,
            )
            .with_metadata(tenant=request.metadata.get("tenant", "default"))
            .build()
        )
        return ctx

    def enrich(self, context: ExecutionContext, data: Dict[str, Any]) -> ExecutionContext:
        """
        Enrich an existing context with additional data.

        Returns a new context instance (immutable).
        """
        if not context:
            raise ManagerValidationError("Context cannot be None")
        return context.update(metadata={**context.metadata, **data})

    def validate(self, context: ExecutionContext) -> None:
        """Validate the context."""
        if not context:
            raise ManagerValidationError("Context cannot be None")
        self._validator.validate(context)

    def persist(self, context: ExecutionContext) -> None:
        """
        Persist the context for traceability.

        Default implementation is a no-op.
        Override for custom persistence (e.g., database, audit log).
        """
        pass
