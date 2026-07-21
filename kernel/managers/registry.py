# kernel/managers/registry.py
"""
Generic registry for manager components.
"""

from typing import Dict, List, Optional, Type, TypeVar
from threading import RLock

from .exceptions import ManagerRegistrationError, ManagerNotFoundError

T = TypeVar('T')


class Registry:
    """
    Thread-safe registry for manager components.

    Generic implementation that can be used by all managers.
    """

    def __init__(self) -> None:
        self._items: Dict[str, T] = {}
        self._lock = RLock()

    def register(self, name: str, item: T) -> None:
        with self._lock:
            if name in self._items:
                raise ManagerRegistrationError(f"Item '{name}' already registered")
            self._items[name] = item

    def get(self, name: str) -> T:
        with self._lock:
            if name not in self._items:
                raise ManagerNotFoundError(f"Item '{name}' not found")
            return self._items[name]

    def has(self, name: str) -> bool:
        with self._lock:
            return name in self._items

    def list(self) -> List[str]:
        with self._lock:
            return list(self._items.keys())

    def clear(self) -> None:
        with self._lock:
            self._items.clear()

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)
