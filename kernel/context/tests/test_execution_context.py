# kernel/context/tests/test_execution_context.py
from datetime import datetime, timezone
from uuid import UUID

from kernel.context import ExecutionContext, RequestContext


class TestExecutionContext:
    def test_creation(self):
        req = RequestContext(identity="alice")
        ctx = ExecutionContext(request=req)
        assert ctx.request == req
        assert isinstance(ctx.execution_id, UUID)
        assert ctx.created_at.tzinfo == timezone.utc
        assert ctx.updated_at.tzinfo == timezone.utc

    def test_update(self):
        req = RequestContext(identity="alice")
        ctx = ExecutionContext(request=req)
        new_req = RequestContext(identity="bob")
        ctx2 = ctx.update(request=new_req)
        assert ctx2.request.identity == "bob"
        assert ctx.request.identity == "alice"
        assert ctx2.updated_at > ctx.updated_at

    def test_to_dict(self):
        req = RequestContext(identity="alice", resource="/doc", operation="read")
        ctx = ExecutionContext(request=req)
        d = ctx.to_dict()
        assert d["request"]["identity"] == "alice"
        assert "execution_id" in d
        assert "created_at" in d
        assert "updated_at" in d
        assert "metadata" in d
