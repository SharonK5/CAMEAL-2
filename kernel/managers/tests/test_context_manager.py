# kernel/managers/tests/test_context_manager.py
import pytest

from kernel.managers import ContextManager
from kernel.models import Request
from kernel.context import RequestContext


class TestContextManager:
    def test_build(self):
        mgr = ContextManager()
        request = Request(identity="alice", resource="/doc", operation="read")
        ctx = mgr.build(request)
        assert ctx.request.identity == "alice"
        assert ctx.request.resource == "/doc"
        assert ctx.request.operation == "read"
        assert ctx.metadata["tenant"] == "default"

    def test_enrich(self):
        mgr = ContextManager()
        request = Request(identity="alice", resource="/doc", operation="read")
        ctx = mgr.build(request)
        ctx2 = mgr.enrich(ctx, {"key": "value"})
        assert ctx2.metadata["key"] == "value"
        assert "key" not in ctx.metadata

    def test_validate(self):
        mgr = ContextManager()
        request = Request(identity="alice", resource="/doc", operation="read")
        ctx = mgr.build(request)
        mgr.validate(ctx)  # Should not raise

        invalid = Request(identity="", resource="", operation="")
        ctx2 = mgr.build(invalid)
        with pytest.raises(Exception, match="Identity is required"):
            mgr.validate(ctx2)
