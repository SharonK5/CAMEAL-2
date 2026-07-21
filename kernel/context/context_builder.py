# kernel/context/context_builder.py
"""
Context builder – constructs execution contexts.
"""

from typing import Any, Dict, Optional
from uuid import UUID

from .execution_context import ExecutionContext
from .request_context import RequestContext
from .security_context import SecurityContext
from .workflow_context import WorkflowContext
from .trace_context import TraceContext
from .provenance_context import ProvenanceContext
from .exceptions import ContextBuilderError


class ContextBuilder:
    """
    Builds immutable execution contexts.
    """

    def __init__(self) -> None:
        self._request: Optional[RequestContext] = None
        self._security: Optional[SecurityContext] = None
        self._workflow: Optional[WorkflowContext] = None
        self._trace: Optional[TraceContext] = None
        self._provenance: Optional[ProvenanceContext] = None
        self._metadata: Dict[str, Any] = {}

    def with_request(
        self,
        request_id: Optional[UUID] = None,
        identity: str = "",
        resource: str = "",
        operation: str = "",
        **kwargs
    ) -> "ContextBuilder":
        self._request = RequestContext(
            request_id=request_id or UUID("00000000-0000-0000-0000-000000000000"),
            identity=identity,
            resource=resource,
            operation=operation,
            **kwargs
        )
        return self

    def with_security(
        self,
        identity: str = "",
        roles: tuple = (),
        permissions: tuple = (),
        authenticated: bool = False,
        **kwargs
    ) -> "ContextBuilder":
        self._security = SecurityContext(
            identity=identity,
            roles=roles,
            permissions=permissions,
            authenticated=authenticated,
            metadata=kwargs
        )
        return self

    def with_workflow(
        self,
        workflow_id: str = "",
        workflow_name: str = "",
        **kwargs
    ) -> "ContextBuilder":
        self._workflow = WorkflowContext(
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            **kwargs
        )
        return self

    def with_trace(
        self,
        trace_id: str = "",
        span_id: str = "",
        **kwargs
    ) -> "ContextBuilder":
        self._trace = TraceContext(
            trace_id=trace_id,
            span_id=span_id,
            **kwargs
        )
        return self

    def with_provenance(self, **kwargs) -> "ContextBuilder":
        self._provenance = ProvenanceContext(**kwargs)
        return self

    def with_metadata(self, **kwargs) -> "ContextBuilder":
        self._metadata.update(kwargs)
        return self

    def build(self) -> ExecutionContext:
        """Build the execution context."""
        if self._request is None:
            raise ContextBuilderError("Request context is required")

        return ExecutionContext(
            request=self._request,
            security=self._security or SecurityContext(),
            workflow=self._workflow or WorkflowContext(),
            trace=self._trace or TraceContext(),
            provenance=self._provenance or ProvenanceContext(),
            metadata=self._metadata,
        )
