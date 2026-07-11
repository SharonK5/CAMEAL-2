"""
kernel.lifecycle
================

Lifecycle manager for the CAMEAL Kernel.

Responsibilities
----------------
- Initialize registered components
- Shutdown components gracefully
- Reset runtime state
- Report component health
- Validate startup sequence

The lifecycle manager delegates component discovery to the
ServiceRegistry and assumes components implement the
KernelComponent lifecycle interface.
"""

from __future__ import annotations

import logging
from typing import Any

from .registry import registry
from .base import KernelComponent

logger = logging.getLogger(__name__)


class LifecycleManager:
    """
    Manages startup, shutdown, reset and health checks for
    registered kernel components.
    """

    def initialize(self) -> None:
        """
        Initialize all registered components.
        """
        logger.info("Initializing kernel components...")

        for name in registry.list_services():

            component: KernelComponent = registry.get(name)

            if not component.initialized:

                logger.info("Initializing %s", name)

                component.initialize()

        logger.info("Kernel initialization complete.")

    def shutdown(self) -> None:
        """
        Gracefully shutdown every registered component.
        """

        logger.info("Shutting down kernel...")

        services = registry.list_services()

        # reverse order

        for name in reversed(services):

            component: KernelComponent = registry.get(name)

            logger.info("Stopping %s", name)

            component.shutdown()

        logger.info("Kernel shutdown complete.")

    def reset(self) -> None:
        """
        Reset every registered component.
        """

        logger.info("Resetting kernel components...")

        for name in registry.list_services():

            component: KernelComponent = registry.get(name)

            component.reset()

        logger.info("Kernel reset complete.")

    def health(self) -> dict[str, Any]:
        """
        Return health status for every registered component.
        """

        report: dict[str, Any] = {}

        for name in registry.list_services():

            component: KernelComponent = registry.get(name)

            report[name] = component.health()

        return report


lifecycle = LifecycleManager()
