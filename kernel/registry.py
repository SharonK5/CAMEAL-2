"""
kernel.registry
===============

Central service registry for the CAMEAL Kernel.

The registry is responsible for:

- Registering system modules
- Discovering services
- Preventing duplicate registrations
- Listing active modules
- Unregistering services
- Health inspection

The registry deliberately contains no business logic.
It only manages service references.
"""

from __future__ import annotations

import logging
from threading import RLock
from typing import Any, Dict, List

from .exceptions import (
    ModuleRegistrationError,
    ModuleNotFoundError,
)

logger = logging.getLogger(__name__)


class ServiceRegistry:
    """
    Central registry for all kernel services.

    Example
    -------
    >>> registry.register("repository", Repository())
    >>> repo = registry.get("repository")
    """

    def __init__(self) -> None:
        self._services: Dict[str, Any] = {}
        self._lock = RLock()

    def register(self, name: str, service: Any) -> None:
        """
        Register a service.

        Parameters
        ----------
        name
            Unique service name.

        service
            Service instance.
        """

        with self._lock:

            if name in self._services:
                raise ModuleRegistrationError(
                    f"Service '{name}' is already registered."
                )

            self._services[name] = service

            logger.info("Registered service: %s", name)

    def unregister(self, name: str) -> None:
        """
        Remove a service.
        """

        with self._lock:

            if name not in self._services:
                raise ModuleNotFoundError(
                    f"Service '{name}' not found."
                )

            del self._services[name]

            logger.info("Unregistered service: %s", name)

    def get(self, name: str) -> Any:
        """
        Retrieve a registered service.
        """

        with self._lock:

            if name not in self._services:
                raise ModuleNotFoundError(
                    f"Service '{name}' not registered."
                )

            return self._services[name]

    def exists(self, name: str) -> bool:
        """
        Check whether a service exists.
        """

        with self._lock:
            return name in self._services

    def list_services(self) -> List[str]:
        """
        Return registered service names.
        """

        with self._lock:
            return sorted(self._services.keys())

    def clear(self) -> None:
        """
        Remove every registered service.
        """

        with self._lock:
            self._services.clear()

            logger.info("Registry cleared.")

    def size(self) -> int:
        """
        Number of registered services.
        """

        with self._lock:
            return len(self._services)

    def health(self) -> Dict[str, Any]:
        """
        Registry health summary.
        """

        with self._lock:

            return {
                "registered_services": self.size(),
                "services": self.list_services(),
            }


# Singleton instance used by the kernel
registry = ServiceRegistry()
