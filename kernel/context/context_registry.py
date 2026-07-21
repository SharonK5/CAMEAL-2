# kernel/context/context_registry.py
"""
Context registry – manages context types.
"""

from typing import Dict, Type
from threading import RLock

from .exceptions import ContextRegistryError, ContextNotFoundError


class ContextRegistry:
    """
    Registry of context types.
    """

    def __init__(self) -> None:
        self._types: Dict[str, Type] = {}
        self._lock = RLock()

    def register(self, name: str, context_type: Type) -> None:
        with self._lock:
            if name in self._types:
                raise ContextRegistryError(f"Context type '{name}' already registered")
            self._types[name] = context_type

    def get(self, name: str) -> Type:
        with self._lock:
            if name not in self._types:
                raise ContextNotFoundError(f"Context type '{name}' not found")
            return self._types[name]

    def list_types(self) -> list:
        with self._lock:
            return list(self._types.keys())

    def clear(self) -> None:
        with self._lock:
            self._types.clear()
