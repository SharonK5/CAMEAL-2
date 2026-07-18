"""
security/services/service_registry.py

Thread-safe registry for Security Services.

The ServiceRegistry maintains metadata about available service classes
without instantiating them. It serves as the authoritative source for
service discovery within the Security Services framework.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import Dict, Iterable, Optional, Type

from .base.service import Service
from .base.exceptions import (
    ServiceRegistrationError,
    ServiceResolutionError,
)


@dataclass(frozen=True, slots=True)
class ServiceDescriptor:
    """
    Immutable description of a registered service.
    """

    name: str

    service_class: Type[Service]

    version: str = "1.0.0"

    description: str = ""

    singleton: bool = True

    dependencies: tuple[str, ...] = field(default_factory=tuple)

    enabled: bool = True


class ServiceRegistry:
    """
    Thread-safe registry of available service implementations.

    Responsibilities
    ----------------
    - Register services
    - Unregister services
    - Discover services
    - Store service metadata

    Does NOT:
    - Instantiate services
    - Manage lifecycle
    - Resolve dependencies
    """

    def __init__(self) -> None:

        self._services: Dict[str, ServiceDescriptor] = {}

        self._lock = RLock()

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(self, descriptor: ServiceDescriptor) -> None:
        """
        Register a service descriptor.
        """

        with self._lock:

            if descriptor.name in self._services:
                raise ServiceRegistrationError(
                    f"Service '{descriptor.name}' "
                    "is already registered."
                )

            self._services[descriptor.name] = descriptor

    def unregister(self, name: str) -> None:
        """
        Remove a service from the registry.
        """

        with self._lock:

            if name not in self._services:
                raise ServiceResolutionError(
                    f"Service '{name}' is not registered."
                )

            del self._services[name]

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(self, name: str) -> ServiceDescriptor:
        """
        Retrieve a registered service descriptor.
        """

        try:
            return self._services[name]

        except KeyError as exc:
            raise ServiceResolutionError(
                f"Unknown service '{name}'."
            ) from exc

    def contains(self, name: str) -> bool:
        """
        Returns True if the service is registered.
        """

        return name in self._services

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def list(self) -> tuple[ServiceDescriptor, ...]:
        """
        Return all registered services.
        """

        return tuple(self._services.values())

    def names(self) -> tuple[str, ...]:
        """
        Return registered service names.
        """

        return tuple(sorted(self._services.keys()))

    def enabled(self) -> tuple[ServiceDescriptor, ...]:
        """
        Return enabled services.
        """

        return tuple(
            descriptor
            for descriptor in self._services.values()
            if descriptor.enabled
        )

    def disabled(self) -> tuple[ServiceDescriptor, ...]:
        """
        Return disabled services.
        """

        return tuple(
            descriptor
            for descriptor in self._services.values()
            if not descriptor.enabled
        )

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all registered services.
        """

        with self._lock:
            self._services.clear()

    def __len__(self) -> int:
        return len(self._services)

    def __contains__(self, name: str) -> bool:
        return self.contains(name)

    def __iter__(self) -> Iterable[ServiceDescriptor]:
        return iter(self.list())

    def __repr__(self) -> str:
        return (
            f"ServiceRegistry("
            f"services={len(self)}, "
            f"registered={self.names()})"
        )
