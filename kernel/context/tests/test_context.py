# kernel/context/tests/test_context.py
import pytest
from datetime import datetime, timezone
from uuid import UUID

from kernel.context import (
    ExecutionContext,
    RequestContext,
    SecurityContext,
    WorkflowContext,
    TraceContext,
    ProvenanceContext,
    ContextBuilder,
    ContextValidator,
    ContextRegistry,
)


class TestContext:
    def test_request_context(self):
        req = RequestContext(identity="alice", resource="/doc", operation="read")
        assert req.identity == "alice"
        assert req.resource == "/doc"
        assert req.operation == "read"
        assert req.timestamp.tzinfo == timezone.utc

    def test_security_context(self):
        sec = SecurityContext(identity="alice", roles=("admin",), permissions=("read", "write"))
        assert sec.has_role("admin") is True
        assert sec.has_permission("read") is True
        assert sec.has_permission("delete") is False

    def test_workflow_context(self):
        wf = WorkflowContext(workflow_name="test_wf")
        wf2 = wf.add_step("step1")
        assert wf2.step_index == 1
        assert wf2.step_history == ["step1"]
        assert wf.step_index == 0

    def test_provenance_context(self):
        prov = ProvenanceContext(confidence=0.95)
        prov2 = prov.add_evidence("evid-1", "test_source", "2024-01-01T00:00:00Z")
        assert len(prov2.evidence_ids) == 1
        assert prov2.confidence == 0.95

    def test_trace_context(self):
        trace = TraceContext(trace_id="trace-123", span_id="span-456")
        assert trace.trace_id == "trace-123"
        assert trace.span_id == "span-456"
        assert trace.sampled is True

    def test_execution_context(self):
        req = RequestContext(identity="alice", resource="/doc", operation="read")
        ctx = ExecutionContext(request=req)
        assert ctx.request.identity == "alice"
        assert ctx.execution_id is not None
        assert ctx.created_at.tzinfo == timezone.utc

    def test_context_builder(self):
        builder = ContextBuilder()
        ctx = (
            builder
            .with_request(identity="alice", resource="/doc", operation="read")
            .with_security(roles=("admin",))
            .with_workflow(workflow_name="test")
            .with_trace(trace_id="trace-123", span_id="span-456")
            .with_provenance(confidence=0.95)
            .with_metadata(tenant="cameal")
            .build()
        )
        assert ctx.request.identity == "alice"
        assert ctx.security.has_role("admin") is True
        assert ctx.workflow.workflow_name == "test"
        assert ctx.trace.trace_id == "trace-123"
        assert ctx.provenance.confidence == 0.95
        assert ctx.metadata["tenant"] == "cameal"

    def test_context_validator(self):
        validator = ContextValidator()
        req = RequestContext(identity="alice", resource="/doc", operation="read")
        ctx = ExecutionContext(request=req)
        validator.validate(ctx)  # Should not raise

        invalid = ExecutionContext(request=RequestContext(identity="", resource="", operation=""))
        with pytest.raises(Exception):
            validator.validate(invalid)

    def test_context_registry(self):
        registry = ContextRegistry()
        registry.register("test", RequestContext)
        assert registry.get("test") == RequestContext
        with pytest.raises(Exception):
            registry.register("test", RequestContext)
        assert "test" in registry.list_types()
        registry.clear()
        assert len(registry.list_types()) == 0
