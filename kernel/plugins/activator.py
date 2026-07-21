# kernel/plugins/activator.py
"""
Plugin activator – registers plugin components into the kernel.
"""

from typing import Any, Dict
from ..providers import ProviderRegistry
from ..managers import EngineManager, WorkflowManager, SchedulerManager
from ..orchestrator import ExecutionPlan
from .exceptions import PluginRegistrationError
from .base.plugin import Plugin


class PluginActivator:
    """
    Activates a plugin by registering its providers, engines, workflows, and schedulers.
    """

    def __init__(
        self,
        provider_registry: ProviderRegistry,
        engine_manager: EngineManager,
        workflow_manager: WorkflowManager,
        scheduler_manager: SchedulerManager,
    ):
        self._provider_registry = provider_registry
        self._engine_manager = engine_manager
        self._workflow_manager = workflow_manager
        self._scheduler_manager = scheduler_manager

    def activate(self, plugin: Plugin) -> None:
        """
        Activate the plugin by calling its register method.
        """
        try:
            plugin.register(
                provider_registry=self._provider_registry,
                engine_manager=self._engine_manager,
                workflow_manager=self._workflow_manager,
                scheduler_manager=self._scheduler_manager,
            )
        except Exception as e:
            raise PluginRegistrationError(
                f"Failed to activate plugin '{plugin.name}': {e}"
            ) from e
