# kernel/managers/manager.py
"""
Base manager class.
"""

from typing import Any, Dict, List, Optional, Type
from abc import ABC, abstractmethod

from ..lifecycle import Lifecycle, HealthStatus
from .registry import Registry
from .validator import Validator
from .exceptions import ManagerError


class Manager(Lifecycle):
    """
    Base class for all kernel managers.

    Provides common functionality for registration, resolution, and lifecycle.
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name
        self._registry = Registry()
        self._validator = Validator()

    @property
    def name(self) -> str:
        return self._name

    def register(self, name: str, item: Any) -> None:
        """Register an item with the manager."""
        self._validator.validate_name(name)
        self._registry.register(name, item)

    def get(self, name: str) -> Any:
        """Get an item by name."""
        return self._registry.get(name)

    def has(self, name: str) -> bool:
        """Check if an item is registered."""
        return self._registry.has(name)

    def list(self) -> List[str]:
        """List all registered items."""
        return self._registry.list()

    def clear(self) -> None:
        """Clear all registrations."""
        self._registry.clear()

    def _on_initialize(self) -> None:
        pass

    def _on_validate(self) -> None:
        pass

    def _on_boot(self) -> None:
        pass

    def _on_start(self) -> None:
        pass

    def _on_stop(self) -> None:
        pass

    def _on_shutdown(self) -> None:
        pass

    def _on_dispose(self) -> None:
        pass

    def _on_fail(self, error: Exception) -> None:
        pass

    def _on_health(self) -> HealthStatus:
        # Default implementation: assume healthy if we're running
        return HealthStatus.HEALTHY if self.state.value == "running" else HealthStatus.UNKNOWN

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name}, state={self.state})"
