# kernel/plugins/base/plugin.py
"""
Base plugin interface.
"""

from abc import ABC, abstractmethod
from typing import Optional

from ...lifecycle import Lifecycle
from ...providers import ProviderRegistry
from ...managers import EngineManager, WorkflowManager, SchedulerManager


class Plugin(Lifecycle, ABC):
    """
    Base class for all CAMEAL plugins.

    A plugin is a self-contained unit that can register:
        - Providers
        - Engines
        - Workflows
        - Schedulers
        - Event listeners

    Plugins participate in the kernel lifecycle and can be
    discovered, loaded, and activated dynamically.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the plugin name."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Return the plugin version."""
        pass

    @abstractmethod
    def register(
        self,
        provider_registry: ProviderRegistry,
        engine_manager: EngineManager,
        workflow_manager: WorkflowManager,
        scheduler_manager: SchedulerManager,
    ) -> None:
        """
        Register all components provided by this plugin.

        Implementations should use the provided registries to
        register providers, engines, workflows, and schedulers.
        """
        pass

    # Optionally override lifecycle hooks
    def on_load(self) -> None:
        """Called after the plugin is loaded (before activation)."""
        pass

    def on_unload(self) -> None:
        """Called before the plugin is unloaded."""
        pass
