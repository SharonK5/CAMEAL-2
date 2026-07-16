import pytest
from unittest.mock import Mock

from query.execution import StageRegistry, StageResolver, ExecutionContext
from query.query_request import QueryRequest
from query.execution.stage import Stage


def test_resolve_returns_all_stages_in_registration_order():
    registry = StageRegistry()
    s1 = Mock(spec=Stage)
    s1.name = "a"
    s2 = Mock(spec=Stage)
    s2.name = "b"
    registry.register(s1)
    registry.register(s2)
    resolver = StageResolver(registry)
    request = Mock(spec=QueryRequest)
    context = ExecutionContext()
    stages = resolver.resolve(request, context)
    assert stages == (s1, s2)
