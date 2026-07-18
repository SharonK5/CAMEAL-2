# kernel/container/cache.py
import threading
from typing import Any, Dict, Optional, Type

from .exceptions import ScopeError
from .scopes import Scope


class Cache:
    def __init__(self) -> None:
        self._singletons: Dict[str, Any] = {}
        self._request_caches: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()

    def _get_key(self, key: Any) -> str:
        if isinstance(key, type):
            return key.__name__
        return str(key)

    def get(self, key: Any, request_id: Optional[str] = None) -> Optional[Any]:
        identifier = self._get_key(key)
        with self._lock:
            if identifier in self._singletons:
                return self._singletons[identifier]
            if request_id:
                request_cache = self._request_caches.get(request_id)
                if request_cache and identifier in request_cache:
                    return request_cache[identifier]
            return None

    def set(self, key: Any, instance: Any, scope: Scope, request_id: Optional[str] = None) -> None:
        identifier = self._get_key(key)
        with self._lock:
            if scope == Scope.SINGLETON:
                self._singletons[identifier] = instance
            elif scope == Scope.REQUEST:
                if not request_id:
                    raise ScopeError("Request ID required for request-scoped instances")
                if request_id not in self._request_caches:
                    self._request_caches[request_id] = {}
                self._request_caches[request_id][identifier] = instance

    def clear_request(self, request_id: str) -> None:
        with self._lock:
            self._request_caches.pop(request_id, None)

    def clear_all(self) -> None:
        with self._lock:
            self._singletons.clear()
            self._request_caches.clear()

    def has_request(self, request_id: str) -> bool:
        with self._lock:
            return request_id in self._request_caches

    def set_request_cache(self, request_id: str) -> None:
        with self._lock:
            if request_id not in self._request_caches:
                self._request_caches[request_id] = {}

    def statistics(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "singletons": len(self._singletons),
                "request_scopes": len(self._request_caches),
            }

    def __repr__(self) -> str:
        with self._lock:
            return f"Cache(singletons={len(self._singletons)}, request_scopes={len(self._request_caches)})"
