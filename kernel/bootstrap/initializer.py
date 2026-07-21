# kernel/bootstrap/initializer.py
"""
Initializes runtime components.
"""

from typing import Any, Dict, List
from ..container import Container
from .exceptions import InitializationError


class Initializer:
    """
    Initializes runtime components in dependency order.
    """

    def __init__(self) -> None:
        self._components: Dict[str, Any] = {}

    def register_component(self, name: str, component: Any) -> None:
        self._components[name] = component

    def initialize(self, container: Container) -> None:
        """Initialize all components."""
        for name, component in self._components.items():
            try:
                if hasattr(component, "initialize"):
                    component.initialize()
            except Exception as e:
                raise InitializationError(f"Failed to initialize {name}: {e}") from e
