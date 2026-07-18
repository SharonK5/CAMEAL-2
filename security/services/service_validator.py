"""
security/services/service_validator.py

Validation framework for Security Services.

The ServiceValidator performs structural and runtime validation of
Security Services before they participate in the application.

Responsibilities
----------------
* Validate service metadata
* Validate lifecycle state
* Validate dependencies
* Validate health
* Validate configuration

The validator never creates or resolves services.
"""

from __future__ import annotations

from typing import Iterable

from .base.lifecycle import HealthStatus, ServiceState
from .base.service import Service
from .base.exceptions import (
    ServiceDependencyError,
    ServiceValidationError,
)


class ServiceValidator:
    """
    Validates Security Services.

    Validators are intentionally stateless and reusable.
    """

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def validate(self, service: Service) -> None:
        """
        Perform complete validation.

        Parameters
        ----------
        service:
            Service instance.

        Raises
        ------
        ServiceValidationError
        """

        self.validate_metadata(service)
        self.validate_dependencies(service)
        self.validate_state(service)
        self.validate_health(service)

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def validate_metadata(self, service: Service) -> None:
        """
        Validate service metadata.
        """

        if not service.name.strip():
            raise ServiceValidationError(
                "Service name cannot be empty."
            )

        if not service.version.strip():
            raise ServiceValidationError(
                f"{service.name}: version cannot be empty."
            )

    # ---------------------------------------------------------
    # Dependencies
    # ---------------------------------------------------------

    def validate_dependencies(self, service: Service) -> None:
        """
        Validate dependency declarations.
        """

        deps = service.dependencies

        if deps is None:
            raise ServiceValidationError(
                f"{service.name}: dependencies cannot be None."
            )

        if not isinstance(deps, tuple):
            raise ServiceValidationError(
                f"{service.name}: dependencies must be a tuple."
            )

        seen = set()

        for dependency in deps:

            if not dependency:

                raise ServiceDependencyError(
                    f"{service.name}: empty dependency."
                )

            if dependency in seen:

                raise ServiceDependencyError(
                    f"{service.name}: duplicate dependency "
                    f"'{dependency}'."
                )

            seen.add(dependency)

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def validate_state(self, service: Service) -> None:
        """
        Validate lifecycle state.
        """

        if not isinstance(service.state, ServiceState):

            raise ServiceValidationError(
                f"{service.name}: invalid lifecycle state."
            )

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def validate_health(self, service: Service) -> None:
        """
        Validate service health.

        Only RUNNING services are required to report
        HEALTHY status.
        """

        if service.state == ServiceState.RUNNING:

            health = service.health_check()

            if health != HealthStatus.HEALTHY:

                raise ServiceValidationError(
                    f"{service.name}: unhealthy service."
                )

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def validate_configuration(
        self,
        required: Iterable[str],
        configuration: dict,
    ) -> None:
        """
        Validate configuration values.

        Parameters
        ----------
        required:
            Required configuration keys.

        configuration:
            Configuration dictionary.
        """

        missing = [
            key
            for key in required
            if key not in configuration
        ]

        if missing:

            raise ServiceValidationError(
                "Missing configuration: "
                + ", ".join(missing)
            )
