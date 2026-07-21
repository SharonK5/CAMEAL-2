# kernel/context/tests/test_context_builder.py
import pytest
from kernel.context import ContextBuilder, RequestContext, SecurityContext, WorkflowContext, TraceContext, ProvenanceContext
from kernel.context.exceptions import ContextBuilderError


class TestContextBuilder:
    def test_builder_requires_request(self):
        builder = ContextBuilder()
        with pytest.raises(ContextBuilderError, match="Request context is required"):
            builder.build()

    def test_builder_defaults(self):
        builder = ContextBuilder()
        ctx = builder.with_request(identity="alice", resource="/doc", operation="read").build()
        assert ctx.request.identity == "alice"
        assert isinstance(ctx.security, SecurityContext)
        assert isinstance(ctx.workflow, WorkflowContext)
        assert isinstance(ctx.trace, TraceContext)
        assert isinstance(ctx.provenance, ProvenanceContext)

    def test_builder_chain(self):
        builder = ContextBuilder()
        ctx = (
            builder
            .with_request(identity="alice", resource="/doc", operation="read")
            .with_security(roles=("admin",))
            .with_workflow(workflow_name="chain_test")
            .with_trace(trace_id="trace-123", span_id="span-456")
            .with_provenance(confidence=0.9)
            .build()
        )
        assert ctx.request.identity == "alice"
        assert ctx.security.roles == ("admin",)
        assert ctx.workflow.workflow_name == "chain_test"
        assert ctx.trace.trace_id == "trace-123"
        assert ctx.provenance.confidence == 0.9
