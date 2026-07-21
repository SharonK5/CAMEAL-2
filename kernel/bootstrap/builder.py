# kernel/bootstrap/builder.py
"""
Builds kernel components.
"""

from typing import Optional

from ..container import Container
from ..events import EventBus
from ..context import ContextBuilder
from ..managers import (
    EngineManager,
    RepositoryManager,
    WorkflowManager,
    ContextManager,
    PluginManager,
    SchedulerManager,
)
from ..orchestrator import Orchestrator
from ..kernel import Kernel
from .configuration import Configuration
from .discovery import Discovery
from .loader import Loader
from .registrar import Registrar
from .validator import Validator


class Builder:
    """
    Builds kernel components.
    """

    def __init__(self, config: Configuration) -> None:
        self._config = config
        self._container: Optional[Container] = None
        self._event_bus: Optional[EventBus] = None
        self._context_builder: Optional[ContextBuilder] = None
        self._engine_manager: Optional[EngineManager] = None
        self._repository_manager: Optional[RepositoryManager] = None
        self._workflow_manager: Optional[WorkflowManager] = None
        self._context_manager: Optional[ContextManager] = None
        self._plugin_manager: Optional[PluginManager] = None
        self._scheduler_manager: Optional[SchedulerManager] = None
        self._orchestrator: Optional[Orchestrator] = None
        self._kernel: Optional[Kernel] = None
        self._managers_built: bool = False

    def build_container(self) -> Container:
        """Build the dependency container."""
        self._container = Container()
        return self._container

    def build_core_services(self) -> None:
        """Build core services."""
        # Guard against duplicate registration
        if self._event_bus is not None:
            return
        if not self._container:
            self.build_container()
        self._event_bus = EventBus()
        self._container.register_singleton(EventBus, self._event_bus)
        self._context_builder = ContextBuilder()
        self._container.register_singleton(ContextBuilder, self._context_builder)

    def build_managers(self) -> None:
        """Build managers."""
        if self._managers_built:
            return  # Avoid duplicate registration

        if not self._container:
            self.build_container()

        self._engine_manager = EngineManager()
        self._container.register_singleton(EngineManager, self._engine_manager)

        self._repository_manager = RepositoryManager()
        self._container.register_singleton(RepositoryManager, self._repository_manager)

        self._workflow_manager = WorkflowManager()
        self._container.register_singleton(WorkflowManager, self._workflow_manager)

        self._context_manager = ContextManager()
        self._container.register_singleton(ContextManager, self._context_manager)

        self._plugin_manager = PluginManager(self._container)
        self._container.register_singleton(PluginManager, self._plugin_manager)

        self._scheduler_manager = SchedulerManager()
        self._container.register_singleton(SchedulerManager, self._scheduler_manager)

        self._managers_built = True

    def register_components(self) -> None:
        """Register components from configuration."""
        if not self._container:
            self.build_container()

        # Ensure managers are built (they will be if not already)
        self.build_managers()

        registrar = Registrar(self._container)

        # Register engines
        engine_registrations = self._config.get("engine_registrations", [])
        if engine_registrations:
            registrar.register_engines(self._engine_manager, engine_registrations)

        # Register repositories
        repo_registrations = self._config.get("repository_registrations", [])
        if repo_registrations:
            registrar.register_repositories(self._repository_manager, repo_registrations)

        # Register workflows
        workflow_registrations = self._config.get("workflow_registrations", [])
        if workflow_registrations:
            registrar.register_workflows(self._workflow_manager, workflow_registrations)

    def build_orchestrator(self) -> Orchestrator:
        """Build the orchestrator."""
        self.build_managers()  # Ensures managers exist

        # ✅ FIX: add context_manager
        self._orchestrator = Orchestrator(
            workflow_manager=self._workflow_manager,
            engine_manager=self._engine_manager,
            context_manager=self._context_manager,
        )
        return self._orchestrator

    def validate_runtime(self) -> None:
        """Validate the runtime."""
        if not self._container:
            self.build_container()

        self.build_managers()

        Validator.validate_runtime(
            self._container,
            self._engine_manager,
            self._repository_manager,
            self._workflow_manager,
            self._context_manager,
            self._plugin_manager,
            self._scheduler_manager,
        )

    def build_kernel(self) -> Kernel:
        """Build the kernel."""
        self.build_core_services()
        self.build_managers()
        self.build_orchestrator()

        self._kernel = Kernel(
            container=self._container,
            event_bus=self._event_bus,
            engine_manager=self._engine_manager,
            repository_manager=self._repository_manager,
            workflow_manager=self._workflow_manager,
            context_manager=self._context_manager,
            plugin_manager=self._plugin_manager,
            scheduler_manager=self._scheduler_manager,
            orchestrator=self._orchestrator,
        )
        return self._kernel

    @property
    def container(self) -> Container:
        return self._container

    @property
    def kernel(self) -> Optional[Kernel]:
        return self._kernel
