"""
===============================================================================
Module: services.service_registry

Service Registry.

Maintains registered CAMEAL services.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from collections.abc import Iterator

from .exceptions import DuplicateServiceError
from .service import Service


class ServiceRegistry:
    """
    Mutable registry of services.
    """

    def __init__(self) -> None:
        self._services: dict[str, Service] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, service: Service) -> None:
        if service.name in self._services:
            raise DuplicateServiceError(
                f"Service '{service.name}' already registered."
            )
        self._services[service.name] = service

    def unregister(self, name: str) -> None:
        self._services.pop(name, None)

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, name: str) -> Service | None:
        return self._services.get(name)

    def contains(self, name: str) -> bool:
        return name in self._services

    # ------------------------------------------------------------------
    # Enumeration
    # ------------------------------------------------------------------

    def identifiers(self) -> tuple[str, ...]:
        return tuple(sorted(self._services.keys()))

    def services(self) -> tuple[Service, ...]:
        return tuple(self._services[name] for name in self.identifiers())

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def clear(self) -> None:
        self._services.clear()

    def size(self) -> int:
        return len(self._services)

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    def __contains__(self, name: str) -> bool:
        return self.contains(name)

    def __len__(self) -> int:
        return self.size()

    def __iter__(self) -> Iterator[Service]:
        return iter(self.services())

    # ------------------------------------------------------------------
    # Read-only view
    # ------------------------------------------------------------------

    @property
    def readonly(self) -> ReadOnlyServiceRegistry:
        return ReadOnlyServiceRegistry(self)


class ReadOnlyServiceRegistry:
    """
    Read-only view of a ServiceRegistry.
    """

    def __init__(self, registry: ServiceRegistry) -> None:
        self._registry = registry

    def get(self, name: str) -> Service | None:
        return self._registry.get(name)

    def contains(self, name: str) -> bool:
        return self._registry.contains(name)

    def identifiers(self) -> tuple[str, ...]:
        return self._registry.identifiers()

    def services(self) -> tuple[Service, ...]:
        return self._registry.services()

    def size(self) -> int:
        return self._registry.size()

    def __contains__(self, name: str) -> bool:
        return self.contains(name)

    def __len__(self) -> int:
        return self.size()

    def __iter__(self) -> Iterator[Service]:
        return iter(self.services())
