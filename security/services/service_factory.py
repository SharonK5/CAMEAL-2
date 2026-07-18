"""
security/services/service_factory.py

Factory responsible for creating Security Service instances.

The ServiceFactory creates service implementations from registered
types while remaining independent of lifecycle management and
dependency resolution.
"""

from __future__ import annotations

from threading import RLock
from typing import Any, Callable, Dict, Optional, Type, TypeVar

from .base.service import Service
from .base.exceptions import (
    ServiceConfigurationError,
    ServiceInitializationError,
)

T = TypeVar("T", bound=Service)


class ServiceFactory:
    """
    Factory responsible for creating service instances.

    Supports:

    * lazy instantiation
    * singleton creation
    * transient creation
    * constructor injection
    """

    def __init__(self) -> None:

        self._constructors: Dict[
            Type[Service],
            Callable[..., Service]
        ] = {}

        self._singletons: Dict[
            Type[Service],
            Service
        ] = {}

        self._lock = RLock()

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        service_type: Type[T],
        constructor: Optional[Callable[..., T]] = None,
    ) -> None:
        """
        Register a constructor for a service.

        If constructor is omitted, the class constructor is used.
        """

        with self._lock:

            self._constructors[service_type] = (
                constructor or service_type
            )

    # ---------------------------------------------------------
    # Creation
    # ---------------------------------------------------------

    def create(
        self,
        service_type: Type[T],
        *,
        singleton: bool = True,
        **kwargs: Any,
    ) -> T:
        """
        Create a service instance.

        Parameters
        ----------
        service_type:
            Service class.

        singleton:
            If True, returns the same instance.

        kwargs:
            Constructor arguments.

        Returns
        -------
        Service
        """

        with self._lock:

            if singleton and service_type in self._singletons:
                return self._singletons[service_type]  # type: ignore

            constructor = self._constructors.get(service_type)

            if constructor is None:
                raise ServiceConfigurationError(
                    f"{service_type.__name__} "
                    "has not been registered."
                )

            try:

                service = constructor(**kwargs)

            except Exception as exc:

                raise ServiceInitializationError(
                    f"Unable to construct "
                    f"{service_type.__name__}"
                ) from exc

            if not isinstance(service, Service):
                raise ServiceConfigurationError(
                    "Constructor did not return a Service."
                )

            if singleton:
                self._singletons[service_type] = service

            return service

    # ---------------------------------------------------------
    # Management
    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all cached singleton instances.
        """
        with self._lock:
            self._singletons.clear()

    def unregister(
        self,
        service_type: Type[Service],
    ) -> None:
        """
        Remove a registered service.
        """
        with self._lock:

            self._constructors.pop(
                service_type,
                None,
            )

            self._singletons.pop(
                service_type,
                None,
            )

    # ---------------------------------------------------------
    # Introspection
    # ---------------------------------------------------------

    def registered_services(self) -> tuple[type[Service], ...]:
        """
        Return registered service types.
        """
        return tuple(self._constructors.keys())

    def is_registered(
        self,
        service_type: Type[Service],
    ) -> bool:
        """
        Determine whether a service is registered.
        """
        return service_type in self._constructors

    def singleton_count(self) -> int:
        """
        Number of cached singleton services.
        """
        return len(self._singletons)

    def __len__(self) -> int:
        return len(self._constructors)

    def __contains__(
        self,
        service_type: Type[Service],
    ) -> bool:
        return self.is_registered(service_type)
