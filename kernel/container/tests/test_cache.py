# kernel/container/tests/test_cache.py
import pytest

from ..cache import Cache
from ..scopes import Scope
from ..exceptions import ScopeError


class TestCache:
    def test_singleton_get_set(self):
        cache = Cache()
        instance = object()
        cache.set(object, instance, Scope.SINGLETON)
        result = cache.get(object)
        assert result is instance

    def test_request_get_set(self):
        cache = Cache()
        instance = object()
        cache.set(object, instance, Scope.REQUEST, request_id="req-1")
        result = cache.get(object, request_id="req-1")
        assert result is instance

    def test_request_scope_isolation(self):
        cache = Cache()
        instance1 = object()
        instance2 = object()
        cache.set(object, instance1, Scope.REQUEST, request_id="req-1")
        cache.set(object, instance2, Scope.REQUEST, request_id="req-2")
        result1 = cache.get(object, request_id="req-1")
        result2 = cache.get(object, request_id="req-2")
        assert result1 is instance1
        assert result2 is instance2
        assert result1 is not result2

    def test_request_requires_id(self):
        cache = Cache()
        with pytest.raises(ScopeError, match="Request ID required"):
            cache.set(object, object(), Scope.REQUEST)

    def test_clear_request(self):
        cache = Cache()
        instance = object()
        cache.set(object, instance, Scope.REQUEST, request_id="req-1")
        cache.clear_request("req-1")
        result = cache.get(object, request_id="req-1")
        assert result is None

    def test_clear_all(self):
        cache = Cache()
        cache.set(object, object(), Scope.SINGLETON)
        cache.set(object, object(), Scope.REQUEST, request_id="req-1")
        cache.clear_all()
        assert cache.get(object) is None
        assert cache.get(object, request_id="req-1") is None

    def test_statistics(self):
        cache = Cache()
        cache.set(object, object(), Scope.SINGLETON)
        cache.set(object, object(), Scope.REQUEST, request_id="req-1")
        cache.set(object, object(), Scope.REQUEST, request_id="req-2")
        stats = cache.statistics()
        assert stats["singletons"] == 1
        assert stats["request_scopes"] == 2
