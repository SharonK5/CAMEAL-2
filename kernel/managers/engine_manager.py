# kernel/managers/engine_manager.py
"""
Engine Manager – coordinates cognitive engines.
"""

from typing import Dict, List, Optional, Tuple, Type
from ..lifecycle import Lifecycle, HealthStatus
from .manager import Manager
from .exceptions import ManagerResolutionError


class EngineManager(Manager):
    """
    Manages cognitive engines.

    Responsibilities:
        - Register engines by name and capabilities.
        - Resolve engines by name or capability.
        - Start and stop all engines.
        - Aggregate health status.
    """

    def __init__(self) -> None:
        super().__init__("engine_manager")
        self._capabilities: Dict[str, str] = {}  # capability -> engine name

    def register(self, name: str, engine: Lifecycle, capabilities: List[str]) -> None:
        """Register an engine with its capabilities."""
        self._validator.validate_name(name)
        self._validator.validate_not_none(engine, "engine")

        super().register(name, engine)
        for cap in capabilities:
            if cap in self._capabilities:
                # Overwrite? We'll keep the first registration.
                # Could be a conflict; we'll raise an error.
                raise ManagerResolutionError(
                    f"Capability '{cap}' already registered by '{self._capabilities[cap]}'"
                )
            self._capabilities[cap] = name

    def get_by_capability(self, capability: str) -> Optional[Lifecycle]:
        """Retrieve an engine by capability."""
        name = self._capabilities.get(capability)
        if name:
            return self._registry.get(name)
        return None

    def has_capability(self, capability: str) -> bool:
        """Check if a capability is available."""
        return capability in self._capabilities

    def start_all(self) -> None:
        """Start all registered engines."""
        for name in self._registry.list():
            engine = self._registry.get(name)
            if engine.state.value in ("created", "initialized", "validated"):
                engine.start()

    def stop_all(self) -> None:
        """Stop all registered engines (reverse order)."""
        for name in reversed(self._registry.list()):
            self._registry.get(name).stop()

    def health_all(self) -> Dict[str, HealthStatus]:
        """Return health status of all engines."""
        return {name: self._registry.get(name).health() for name in self._registry.list()}

    def __len__(self) -> int:
        return len(self._registry)
