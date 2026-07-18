"""
security/services/service_manager.py

Central facade for the Security Services framework.

Coordinates service registration, validation, dependency resolution,
lifecycle management, and health monitoring.

The manager delegates work to the Registry, Factory, Resolver,
and Validator and does not implement their responsibilities directly.
"""

from __future__ import annotations

from typing import Dict, Iterable, Optional

from .base.lifecycle import HealthStatus
from .base.service import Service
from .base.exceptions import (
    ServiceResolutionError,
)

from .service_registration import ServiceRegistration
from .service_registry import ServiceRegistry
from .service_factory import ServiceFactory
from .service_resolver import ServiceResolver
from .service_validator import ServiceValidator


class ServiceManager:
    """
    High-level facade over the Security Services framework.
    """

    def __init__(
        self,
        registry: Optional[ServiceRegistry] = None,
        factory: Optional[ServiceFactory] = None,
        resolver: Optional[ServiceResolver] = None,
        validator: Optional[ServiceValidator] = None,
    ) -> None:

        self._registry = registry or ServiceRegistry()

        self._factory = factory or ServiceFactory()

        self._resolver = resolver or ServiceResolver(
            registry=self._registry,
            factory=self._factory,
        )

        self._validator = validator or ServiceValidator(
            registry=self._registry
        )

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, registration: ServiceRegistration) -> None:
        """
        Register a service.
        """
        self._registry.register(registration)

    def unregister(self, name: str) -> None:
        """
        Remove a service registration.
        """
        self._registry.unregister(name)

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def resolve(self, name: str) -> Service:
        """
        Resolve a service instance.
        """
        return self._resolver.resolve(name)

    def try_resolve(self, name: str) -> Optional[Service]:
        """
        Resolve a service or return None.
        """
        try:
            return self.resolve(name)
        except ServiceResolutionError:
            return None

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> None:
        """
        Validate all registered services.
        """
        self._validator.validate()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def initialize_all(self) -> None:
        """
        Initialize every registered service.
        """
        for service in self.services():
            service.initialize()

    def validate_all(self) -> None:
        """
        Validate every initialized service.
        """
        for service in self.services():
            service.validate()

    def start_all(self) -> None:
        """
        Start every validated service.
        """
        for service in self.services():
            service.start()

    def stop_all(self) -> None:
        """
        Stop every running service.
        """
        for service in reversed(list(self.services())):
            service.stop()

    def shutdown_all(self) -> None:
        """
        Shutdown every service.
        """
        for service in reversed(list(self.services())):
            service.shutdown()

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def health(self) -> Dict[str, HealthStatus]:
        """
        Return the health of every resolved service.
        """
        return {
            service.name: service.health_check()
            for service in self.services()
        }

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def services(self) -> Iterable[Service]:
        """
        Iterate over resolved services.
        """
        for registration in self._registry.registrations():
            yield self.resolve(registration.name)

    def registrations(self) -> Iterable[ServiceRegistration]:
        """
        Return all registrations.
        """
        return self._registry.registrations()

    def contains(self, name: str) -> bool:
        """
        Determine whether a service is registered.
        """
        return self._registry.contains(name)

    def count(self) -> int:
        """
        Number of registered services.
        """
        return self._registry.count()

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def __contains__(self, name: str) -> bool:
        return self.contains(name)

    def __len__(self) -> int:
        return self.count()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"services={self.count()})"
        )
