# kernel/kernel.py
"""
CAMEAL Kernel – main runtime entry point.
"""

from typing import Optional, Dict, Any
from .container import Container
from .events import EventBus, KernelStarted, KernelStopped
from .managers import (
    EngineManager,
    RepositoryManager,
    WorkflowManager,
    ContextManager,
    PluginManager,
    SchedulerManager,
)
from .orchestrator import Orchestrator
from .lifecycle import Lifecycle, HealthStatus, LifecycleState
from .models import Request, Response
from .exceptions import ExecutionError


class Kernel(Lifecycle):
    """Main runtime entry point for CAMEAL."""

    def __init__(
        self,
        container: Container,
        event_bus: EventBus,
        engine_manager: EngineManager,
        repository_manager: RepositoryManager,
        workflow_manager: WorkflowManager,
        context_manager: ContextManager,
        plugin_manager: PluginManager,
        scheduler_manager: SchedulerManager,
        orchestrator: Orchestrator,
    ) -> None:
        super().__init__()
        self._container = container
        self._event_bus = event_bus
        self._engine_manager = engine_manager
        self._repository_manager = repository_manager
        self._workflow_manager = workflow_manager
        self._context_manager = context_manager
        self._plugin_manager = plugin_manager
        self._scheduler_manager = scheduler_manager
        self._orchestrator = orchestrator
        self._running = False

    # ---------- Implementation of Lifecycle abstract methods ----------
    def _on_health(self) -> bool:
        """
        Lifecycle health check.

        Returns:
            True if the kernel is healthy, False otherwise.
        """
        # Use the public health() method to determine overall health.
        return self.health() == HealthStatus.HEALTHY

    # ---------- Public API ----------
    def boot(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.discover()
        self.validate()
        self.initialize()

    def execute(self, request: Request) -> Response:
        if not self._running:
            raise ExecutionError("Kernel is not running")
        return self._orchestrator.execute(request)

    def start(self) -> None:
        self._engine_manager.start_all()
        self._repository_manager.start_all()
        self._plugin_manager.start_all()
        self._scheduler_manager.start_all()
        self._running = True
        super().start()
        self._event_bus.publish(KernelStarted())

    def stop(self) -> None:
        self._running = False
        self._scheduler_manager.stop_all()
        self._plugin_manager.stop_all()
        self._repository_manager.stop_all()
        self._engine_manager.stop_all()
        super().stop()
        self._event_bus.publish(KernelStopped())

    def health(self) -> HealthStatus:
        engine_health = self._engine_manager.health_all()
        repo_health = self._repository_manager.health_all()
        all_statuses = list(engine_health.values()) + list(repo_health.values())
        if all(s == HealthStatus.HEALTHY for s in all_statuses):
            return HealthStatus.HEALTHY
        if any(s == HealthStatus.UNHEALTHY for s in all_statuses):
            return HealthStatus.UNHEALTHY
        return HealthStatus.DEGRADED

    def diagnostics(self) -> Dict[str, Any]:
        return {
            "state": self.state.value,
            "running": self._running,
            "engines": self._engine_manager.list(),
            "repositories": self._repository_manager.list(),
            "plugins": self._plugin_manager.list(),
            "health": self.health().value,
        }

    @property
    def container(self) -> Container:
        return self._container
