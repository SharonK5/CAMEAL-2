# kernel/plugins/base/plugin.py
"""
Abstract base class for all plugins.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from ...lifecycle import Lifecycle
from ...providers import ProviderRegistry
from ...managers import EngineManager, WorkflowManager, SchedulerManager


class Plugin(Lifecycle, ABC):
    """
    Base interface for all plugins.

    A plugin is a self-contained extension that can register:
        - Providers
        - Engines
        - Workflows
        - Schedulers
        - Event handlers

    Plugins are discovered, loaded, and activated during kernel startup.
    They participate in the standard lifecycle (start/stop/health).

    Every plugin must implement:
        - register() – to register its components with the kernel's managers.
        - start() – to start any background tasks or connections.
        - stop() – to clean up resources.
    """

    @abstractmethod
    def register(
        self,
        provider_registry: ProviderRegistry,
        engine_manager: EngineManager,
        workflow_manager: WorkflowManager,
        scheduler_manager: SchedulerManager,
    ) -> None:
        """
        Register the plugin's components with the kernel.

        Args:
            provider_registry: The registry for providers.
            engine_manager: Manager for engines.
            workflow_manager: Manager for workflows.
            scheduler_manager: Manager for schedulers.
        """
        pass

    def configure(self, config: Dict[str, Any]) -> None:
        """
        Apply configuration to the plugin.

        This method is called after instantiation but before registration.
        Override it to accept plugin-specific settings.

        Args:
            config: Dictionary of configuration values.
        """
        pass

    def on_load(self) -> None:
        """
        Called immediately after the plugin is loaded.
        Can be overridden for any pre‑registration setup.
        """
        pass
