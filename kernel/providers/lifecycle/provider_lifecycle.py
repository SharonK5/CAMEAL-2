# kernel/providers/lifecycle/provider_lifecycle.py
"""
Lifecycle management for providers.

This module provides utility functions for managing the lifecycle
of provider collections. It is used by the kernel to start, stop,
and monitor all registered providers consistently.

The lifecycle follows the same pattern as other kernel components:
    - Providers are started in registration order
    - Providers are stopped in reverse order (dependencies first)
    - Health checks are aggregated for monitoring
"""

from typing import List, Dict, Optional
import logging

from ...lifecycle import Lifecycle, HealthStatus
from ..base.provider import Provider

logger = logging.getLogger(__name__)


class ProviderLifecycle:
    """
    Manages the lifecycle of all registered providers.

    This class provides convenience methods to start, stop, and
    check the health of all providers in a registry.

    It is typically used by the kernel during startup and shutdown:

        # During bootstrap:
        providers = registry.all()
        ProviderLifecycle.start_all(providers)

        # During shutdown:
        ProviderLifecycle.stop_all(providers)

    The class is stateless and operates on provider collections
    passed to it.
    """

    @staticmethod
    def start_all(providers: List[Provider]) -> None:
        """
        Start all providers in the given list.

        Providers are started in the order they appear in the list.
        If any provider fails to start, the exception is raised
        and subsequent providers are not started.

        Args:
            providers: List of provider instances.

        Raises:
            Exception: Propagates the first start failure.
        """
        if not providers:
            logger.debug("No providers to start")
            return

        logger.info(f"Starting {len(providers)} provider(s)")

        for provider in providers:
            provider_name = repr(provider)
            logger.debug(f"Starting provider: {provider_name}")
            try:
                provider.start()
            except Exception as e:
                logger.error(f"Failed to start provider {provider_name}: {e}")
                raise

        logger.info(f"All {len(providers)} provider(s) started successfully")

    @staticmethod
    def stop_all(providers: List[Provider]) -> None:
        """
        Stop all providers in reverse order.

        Stopping in reverse order ensures that dependencies are
        stopped before their dependents (if providers depend on
        each other, which is uncommon but possible).

        If a provider fails to stop, the error is logged but
        other providers continue to be stopped.

        Args:
            providers: List of provider instances.
        """
        if not providers:
            logger.debug("No providers to stop")
            return

        logger.info(f"Stopping {len(providers)} provider(s)")

        stopped = 0
        failed = 0

        for provider in reversed(providers):
            provider_name = repr(provider)
            try:
                logger.debug(f"Stopping provider: {provider_name}")
                provider.stop()
                stopped += 1
            except Exception as e:
                logger.error(f"Error stopping provider {provider_name}: {e}")
                failed += 1

        if failed > 0:
            logger.warning(
                f"Stopped {stopped} provider(s), {failed} failed"
            )
        else:
            logger.info(f"All {len(providers)} provider(s) stopped successfully")

    @staticmethod
    def health_all(providers: List[Provider]) -> Dict[str, HealthStatus]:
        """
        Return health status for all providers.

        Each provider's `health()` method is called. If a provider
        raises an exception during the health check, it is treated
        as UNHEALTHY and the error is logged.

        Args:
            providers: List of provider instances.

        Returns:
            A dictionary mapping provider representation to HealthStatus.
        """
        result = {}
        for provider in providers:
            provider_name = repr(provider)
            try:
                result[provider_name] = provider.health()
            except Exception as e:
                logger.error(f"Health check failed for {provider_name}: {e}")
                result[provider_name] = HealthStatus.UNHEALTHY
        return result

    @staticmethod
    def is_healthy(providers: List[Provider]) -> bool:
        """
        Check if all providers are healthy.

        This is a convenience wrapper around `health_all()`.

        Args:
            providers: List of provider instances.

        Returns:
            True if all providers are HEALTHY, False otherwise.
        """
        if not providers:
            return True
        statuses = ProviderLifecycle.health_all(providers)
        return all(s == HealthStatus.HEALTHY for s in statuses.values())

    @staticmethod
    def get_unhealthy(providers: List[Provider]) -> List[str]:
        """
        Return the names of all unhealthy providers.

        Args:
            providers: List of provider instances.

        Returns:
            A list of provider names that are not HEALTHY.
        """
        statuses = ProviderLifecycle.health_all(providers)
        return [name for name, status in statuses.items() if status != HealthStatus.HEALTHY]

    @staticmethod
    def summary(providers: List[Provider]) -> Dict[str, any]:
        """
        Return a summary of provider health status.

        Args:
            providers: List of provider instances.

        Returns:
            A dictionary containing:
                - total: Total number of providers
                - healthy: Number of healthy providers
                - unhealthy: Number of unhealthy providers
                - details: Dictionary of individual statuses
        """
        statuses = ProviderLifecycle.health_all(providers)
        total = len(statuses)
        unhealthy = [s for s in statuses.values() if s != HealthStatus.HEALTHY]
        return {
            "total": total,
            "healthy": total - len(unhealthy),
            "unhealthy": len(unhealthy),
            "details": statuses,
        }
