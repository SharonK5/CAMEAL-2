"""
security/services/service_resolver.py

Service dependency resolution for the CAMEAL Security Services Framework.

The ServiceResolver is responsible for resolving registered services,
their dependencies, and returning initialized service instances.

It does not create or register services; those responsibilities belong
to the ServiceFactory and ServiceRegistry respectively.
"""

from __future__ import annotations

from threading import RLock
from typing import Dict, Iterable, Optional

from .base.service import Service
from .base.exceptions import (
    ServiceDependencyError,
    ServiceResolutionError,
)
from .service_registry import ServiceRegistry


class ServiceResolver:
    """
    Resolves registered security services.

    Parameters
    ----------
    registry:
        Registry containing service instances.
    """

    def __init__(self, registry: ServiceRegistry):

        self._registry = registry
        self._lock = RLock()

    # ---------------------------------------------------------
    # Basic Resolution
    # ---------------------------------------------------------

    def resolve(self, name: str) -> Service:
        """
        Resolve a registered service.

        Parameters
        ----------
        name:
            Service name.

        Returns
        -------
        Service

        Raises
        ------
        ServiceResolutionError
        """

        with self._lock:

            service = self._registry.get(name)

            if service is None:
                raise ServiceResolutionError(
                    f"Service '{name}' is not registered."
                )

            return service

    def exists(self, name: str) -> bool:
        """
        Check whether a service exists.
        """
        return self._registry.contains(name)

    # ---------------------------------------------------------
    # Dependency Resolution
    # ---------------------------------------------------------

    def resolve_dependencies(
        self,
        service: Service,
    ) -> Dict[str, Service]:
        """
        Resolve dependencies declared by a service.

        Parameters
        ----------
        service:
            Service whose dependencies should be resolved.

        Returns
        -------
        dict[str, Service]
        """

        resolved: Dict[str, Service] = {}

        for dependency in service.dependencies:

            dependency_service = self.resolve(dependency)

            resolved[dependency] = dependency_service

        return resolved

    def validate_dependencies(
        self,
        service: Service,
    ) -> None:
        """
        Ensure all dependencies are registered.

        Raises
        ------
        ServiceDependencyError
        """

        for dependency in service.dependencies:

            if not self.exists(dependency):

                raise ServiceDependencyError(
                    f"Missing dependency "
                    f"'{dependency}' "
                    f"for service '{service.name}'."
                )

    # ---------------------------------------------------------
    # Bulk Operations
    # ---------------------------------------------------------

    def resolve_all(self) -> Dict[str, Service]:
        """
        Return all registered services.
        """

        return {
            service.name: service
            for service in self._registry.services()
        }

    def resolve_many(
        self,
        names: Iterable[str],
    ) -> Dict[str, Service]:
        """
        Resolve multiple services.

        Parameters
        ----------
        names:
            Iterable of service names.

        Returns
        -------
        dict[str, Service]
        """

        resolved = {}

        for name in names:

            resolved[name] = self.resolve(name)

        return resolved

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def registry(self) -> ServiceRegistry:
        """
        Underlying registry.
        """
        return self._registry

    def __len__(self) -> int:
        return len(self._registry)

    def __contains__(self, name: str) -> bool:
        return self.exists(name)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(services={len(self)})"
        )
