# kernel/bootstrap/bootstrap.py
"""
Main bootstrap class – initializes the kernel runtime.
"""

import logging
from typing import Any, Dict, Optional, Union

from .configuration import Configuration
from .builder import Builder
from .exceptions import BootstrapError
from ..kernel import Kernel

logger = logging.getLogger(__name__)


class Bootstrap:
    """
    Bootstraps the CAMEAL Kernel.

    Responsibilities:
        - Load configuration.
        - Build kernel components.
        - Register services.
        - Validate runtime.
        - Return a running kernel.

    Usage:
        bootstrap = Bootstrap()
        kernel = bootstrap.bootstrap(config)
        kernel.start()
    """

    def __init__(self) -> None:
        self._config = Configuration()
        self._builder: Optional[Builder] = None

    def bootstrap(self, config_source: Optional[Union[Dict[str, Any], str]] = None) -> Kernel:
        """
        Bootstrap the kernel.

        Args:
            config_source: Configuration source (dict or file path).

        Returns:
            A fully initialized Kernel instance.
        """
        try:
            # Load configuration
            if config_source:
                self._config.load(config_source)

            # Build components
            self._builder = Builder(self._config)

            # Build container and core services
            self._builder.build_container()
            self._builder.build_core_services()
            self._builder.build_managers()

            # Register components
            self._builder.register_components()

            # Build orchestrator
            self._builder.build_orchestrator()

            # Validate runtime
            self._builder.validate_runtime()

            # Build and return kernel
            kernel = self._builder.build_kernel()

            logger.info("Kernel bootstrapped successfully")
            return kernel

        except Exception as e:
            logger.error(f"Bootstrap failed: {e}")
            raise BootstrapError(f"Failed to bootstrap kernel: {e}") from e
